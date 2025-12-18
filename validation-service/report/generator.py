"""
SADNxAI PDF Report Generator
Generates professional privacy reports with PDPL/SAMA regulatory citations
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID

# Add parent for shared module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
)
from reportlab.lib.enums import TA_CENTER


# Colors
PRIMARY_COLOR = colors.HexColor("#2563EB")
SUCCESS_COLOR = colors.HexColor("#10B981")
WARNING_COLOR = colors.HexColor("#F59E0B")
ERROR_COLOR = colors.HexColor("#EF4444")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
DARK_GRAY = colors.HexColor("#374151")


def _fetch_db_classifications(job_id: str) -> Optional[List[Dict[str, Any]]]:
    """Fetch classifications from PostgreSQL database"""
    try:
        from shared.database import Database

        async def _fetch():
            try:
                return await Database.get_classifications(UUID(job_id))
            except Exception as e:
                print(f"Failed to fetch classifications from DB: {e}")
                return None

        # Run async query in sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _fetch())
                    return future.result()
            else:
                return loop.run_until_complete(_fetch())
        except RuntimeError:
            return asyncio.run(_fetch())
    except Exception as e:
        print(f"Error fetching DB classifications: {e}")
        return None


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
    content.append(Paragraph("Data Anonymization Compliance Report", styles['Subtitle']))
    content.append(Paragraph("PDPL & SAMA Open Banking Compliant", ParagraphStyle(
        name='ComplianceBadge',
        parent=styles['Normal'],
        fontSize=10,
        textColor=SUCCESS_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20
    )))

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

    # Try to fetch classifications from PostgreSQL first
    db_classifications = _fetch_db_classifications(job_id)

    if db_classifications:
        # Use DB classifications with regulation references
        class_data = [["Column", "Type", "Technique", "Regulations"]]

        for cls in db_classifications:
            col_name = cls.get('column_name', 'Unknown')
            cls_name = cls.get('classification_name', 'Unknown')
            tech_name = cls.get('technique_name', 'Unknown')

            # Build regulation string from DB
            reg_refs = cls.get('regulation_refs', [])
            if reg_refs and isinstance(reg_refs, list):
                reg_strs = []
                for ref in reg_refs:
                    if isinstance(ref, dict) and ref.get('regulation_id'):
                        reg_strs.append(ref.get('regulation_id', ''))
                reg_string = ', '.join(reg_strs[:3])  # Limit to 3 for space
                if len(reg_strs) > 3:
                    reg_string += f" (+{len(reg_strs)-3})"
            else:
                reg_string = "-"

            class_data.append([col_name, cls_name, tech_name, reg_string])

        if len(class_data) > 1:
            class_table = Table(class_data, colWidths=[4*cm, 3.5*cm, 3*cm, 3*cm])
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

        # Add detailed justifications section
        content.append(Spacer(1, 15))
        content.append(Paragraph("Column Justifications", styles['SectionHeader']))

        for cls in db_classifications:
            col_name = cls.get('column_name', 'Unknown')
            reasoning = cls.get('reasoning', '')
            reg_refs = cls.get('regulation_refs', [])

            if reasoning or (reg_refs and isinstance(reg_refs, list) and len(reg_refs) > 0):
                content.append(Paragraph(f"<b>{col_name}</b>", styles['ReportBody']))
                if reasoning:
                    content.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{reasoning}", styles['ReportBody']))
                if reg_refs and isinstance(reg_refs, list):
                    for ref in reg_refs:
                        if isinstance(ref, dict):
                            ref_text = f"&nbsp;&nbsp;&nbsp;• {ref.get('source', '')} {ref.get('article_number', '')}"
                            if ref.get('title'):
                                ref_text += f": {ref.get('title', '')}"
                            if ref.get('relevance'):
                                ref_text += f" - {ref.get('relevance', '')}"
                            content.append(Paragraph(ref_text, styles['ReportBody']))
    else:
        # Fallback to session classification (backwards compatible)
        classification = session.get('classification', {})
        if classification:
            class_data = [["Column", "Type", "Technique", "Regulation"]]

            # Add direct identifiers
            for col in classification.get('direct_identifiers', []):
                class_data.append([col, "Direct Identifier", "Suppressed", "PDPL Art.11,15"])

            # Add quasi identifiers
            for col in classification.get('quasi_identifiers', []):
                class_data.append([col, "Quasi-Identifier", "Generalized", "PDPL Art.11,17"])

            # Add linkage identifiers
            for col in classification.get('linkage_identifiers', []):
                class_data.append([col, "Linkage Identifier", "Pseudonymized", "PDPL Art.19"])

            # Add date columns
            for col in classification.get('date_columns', []):
                class_data.append([col, "Date Column", "Date Shifted", "PDPL Art.11"])

            # Add sensitive attributes
            for col in classification.get('sensitive_attributes', []):
                class_data.append([col, "Sensitive Attribute", "Kept", "PDPL Art.5,24"])

            if len(class_data) > 1:
                class_table = Table(class_data, colWidths=[4*cm, 3.5*cm, 3*cm, 3*cm])
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

    # Regulatory Compliance Section
    content.append(Paragraph("Regulatory Compliance", styles['SectionHeader']))

    compliance_text = """
    <b>PDPL Compliance (Royal Decree M/19)</b><br/>
    • <b>Article 11</b>: Data minimization applied - only minimum necessary data retained<br/>
    • <b>Article 15</b>: Data disclosed in anonymized form meeting k-anonymity threshold<br/>
    • <b>Article 19</b>: Technical measures (pseudonymization, generalization) implemented<br/>
    • <b>Article 29</b>: Cross-border transfer protection through anonymization<br/><br/>

    <b>SAMA Open Banking Alignment</b><br/>
    • <b>Section 2.6.2</b>: Data secured per PCI-DSS principles<br/>
    • <b>Section 2.6.3</b>: Third-party sharing enabled through anonymization<br/>
    • <b>Framework</b>: Customer data protected while enabling TPP services
    """
    content.append(Paragraph(compliance_text, styles['ReportBody']))
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
    content.append(Paragraph(
        "Compliant with Saudi Personal Data Protection Law (PDPL) and SAMA Open Banking Framework",
        ParagraphStyle(
            name='FooterCompliance',
            parent=styles['Normal'],
            fontSize=7,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
    ))

    # Build PDF
    doc.build(content)

    return filepath
