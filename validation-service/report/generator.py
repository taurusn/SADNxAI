"""
PDF Report Generator
Generates professional privacy reports using ReportLab
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# Colors
PRIMARY_COLOR = colors.HexColor("#2563EB")
SUCCESS_COLOR = colors.HexColor("#10B981")
WARNING_COLOR = colors.HexColor("#F59E0B")
ERROR_COLOR = colors.HexColor("#EF4444")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
DARK_GRAY = colors.HexColor("#374151")


def generate_pdf_report(
    output_path: str,
    session: Dict[str, Any],
    validation_result: Dict[str, Any],
    job_id: str
) -> str:
    """
    Generate a PDF privacy report.

    Args:
        output_path: Directory to save the report
        session: Session data including classification
        validation_result: Validation metrics and results
        job_id: Unique job identifier

    Returns:
        Path to generated PDF file
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Generate filename
    filename = f"{job_id}_privacy_report.pdf"
    filepath = os.path.join(output_path, filename)

    # Create document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles - use unique names to avoid conflicts
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=30
    ))

    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name='PassedStatus',
        parent=styles['Normal'],
        fontSize=16,
        textColor=SUCCESS_COLOR,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='FailedStatus',
        parent=styles['Normal'],
        fontSize=16,
        textColor=ERROR_COLOR,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10
    ))

    # Build document content
    content = []

    # Header
    content.append(Paragraph("SADNxAI", styles['ReportTitle']))
    content.append(Paragraph("Privacy Anonymization Report", styles['Subtitle']))

    # Report info
    content.append(HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY))
    content.append(Spacer(1, 10))

    # Meta information table
    meta_data = [
        ["Report Date:", datetime.now().strftime("%Y-%m-%d %H:%M")],
        ["Session ID:", session.get('id', job_id)[:12] + "..."],
        ["File:", session.get('title', 'Unknown')],
        ["Records Processed:", str(session.get('row_count', 'N/A'))],
    ]

    meta_table = Table(meta_data, colWidths=[3*cm, 10*cm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(meta_table)
    content.append(Spacer(1, 20))

    # Status
    passed = validation_result.get('passed', False)
    status_style = 'PassedStatus' if passed else 'FailedStatus'
    status_text = "✓ VALIDATION PASSED" if passed else "✗ VALIDATION FAILED"
    content.append(Paragraph(status_text, styles[status_style]))
    content.append(Spacer(1, 20))

    # Classification Summary
    content.append(Paragraph("Classification Summary", styles['SectionHeader']))

    classification = session.get('classification', {})
    if classification:
        class_data = [["Column", "Type", "Technique"]]

        # Add direct identifiers
        for col in classification.get('direct_identifiers', []):
            class_data.append([col, "Direct Identifier", "Suppressed"])

        # Add quasi identifiers
        for col in classification.get('quasi_identifiers', []):
            class_data.append([col, "Quasi-Identifier", "Generalized"])

        # Add linkage identifiers
        for col in classification.get('linkage_identifiers', []):
            class_data.append([col, "Linkage Identifier", "Pseudonymized"])

        # Add date columns
        for col in classification.get('date_columns', []):
            class_data.append([col, "Date Column", "Date Shifted"])

        # Add sensitive attributes
        for col in classification.get('sensitive_attributes', []):
            class_data.append([col, "Sensitive Attribute", "Kept"])

        if len(class_data) > 1:
            class_table = Table(class_data, colWidths=[5*cm, 4.5*cm, 4*cm])
            class_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            content.append(class_table)
    else:
        content.append(Paragraph("No classification data available.", styles['ReportBody']))

    content.append(Spacer(1, 20))

    # Privacy Metrics
    content.append(Paragraph("Privacy Metrics", styles['SectionHeader']))

    metrics = validation_result.get('metrics', {})

    def get_metric_status(metric_data: Dict) -> str:
        if metric_data.get('passed', False):
            return "✓"
        return "✗"

    def get_metric_color(metric_data: Dict) -> colors.Color:
        if metric_data.get('passed', False):
            return SUCCESS_COLOR
        return ERROR_COLOR

    metrics_data = [["Metric", "Value", "Threshold", "Status"]]

    # k-anonymity
    k_metric = metrics.get('k_anonymity', {})
    metrics_data.append([
        "k-Anonymity",
        str(k_metric.get('value', 'N/A')),
        f"≥ {k_metric.get('threshold', 'N/A')}",
        get_metric_status(k_metric)
    ])

    # l-diversity
    l_metric = metrics.get('l_diversity', {})
    metrics_data.append([
        "l-Diversity",
        str(l_metric.get('value', 'N/A')),
        f"≥ {l_metric.get('threshold', 'N/A')}",
        get_metric_status(l_metric)
    ])

    # t-closeness
    t_metric = metrics.get('t_closeness', {})
    metrics_data.append([
        "t-Closeness",
        str(t_metric.get('value', 'N/A')),
        f"≤ {t_metric.get('threshold', 'N/A')}",
        get_metric_status(t_metric)
    ])

    # Risk score
    risk_metric = metrics.get('risk_score', {})
    metrics_data.append([
        "Risk Score",
        f"{risk_metric.get('value', 'N/A')}%",
        f"< {risk_metric.get('threshold', 'N/A')}%",
        get_metric_status(risk_metric)
    ])

    metrics_table = Table(metrics_data, colWidths=[4*cm, 3*cm, 3*cm, 2*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Color the status cells
    for i, metric in enumerate(['k_anonymity', 'l_diversity', 't_closeness', 'risk_score'], start=1):
        metric_data = metrics.get(metric, {})
        color = SUCCESS_COLOR if metric_data.get('passed', False) else ERROR_COLOR
        metrics_table.setStyle(TableStyle([
            ('TEXTCOLOR', (3, i), (3, i), color),
            ('FONTNAME', (3, i), (3, i), 'Helvetica-Bold'),
        ]))

    content.append(metrics_table)
    content.append(Spacer(1, 20))

    # Remediation suggestions (if any)
    failed_metrics = validation_result.get('failed_metrics', [])
    suggestions = validation_result.get('remediation_suggestions', [])

    if failed_metrics or suggestions:
        content.append(Paragraph("Remediation Suggestions", styles['SectionHeader']))

        if suggestions:
            for suggestion in suggestions:
                bullet_text = f"• <b>{suggestion.get('metric', 'Unknown')}:</b> {suggestion.get('suggestion', '')}"
                content.append(Paragraph(bullet_text, styles['ReportBody']))
        else:
            for metric in failed_metrics:
                content.append(Paragraph(f"• {metric} threshold not met", styles['ReportBody']))

        content.append(Spacer(1, 20))

    # Footer
    content.append(HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY))
    content.append(Spacer(1, 10))
    content.append(Paragraph(
        f"Generated by SADNxAI v1.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
    ))

    # Build PDF
    doc.build(content)

    return filepath
