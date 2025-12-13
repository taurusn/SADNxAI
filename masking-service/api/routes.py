"""
Masking Service API Routes
"""

import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.models import Classification

from engine.suppressor import Suppressor
from engine.date_shifter import DateShifter
from engine.generalizer import Generalizer
from engine.pseudonymizer import Pseudonymizer
from engine.text_scrubber import TextScrubber


router = APIRouter()

# Storage paths
STORAGE_PATH = os.getenv("STORAGE_PATH", "/storage")
INPUT_PATH = os.path.join(STORAGE_PATH, "input")
STAGING_PATH = os.path.join(STORAGE_PATH, "staging")
OUTPUT_PATH = os.path.join(STORAGE_PATH, "output")


class MaskingRequest(BaseModel):
    """Request model for masking endpoint"""
    job_id: str
    input_path: str
    classification: Classification
    salt: str


class MaskingResponse(BaseModel):
    """Response model for masking endpoint"""
    output_path: str
    techniques_applied: Dict[str, str]
    rows_processed: int
    columns_masked: int


@router.post("/mask", response_model=MaskingResponse)
async def mask_data(request: MaskingRequest) -> MaskingResponse:
    """
    Apply masking techniques to a CSV file.

    The masking pipeline runs in order:
    1. Suppress - Remove direct identifiers
    2. Date Shift - Apply random offset to dates
    3. Generalize - Apply hierarchies to quasi-identifiers
    4. Pseudonymize - Hash linkage identifiers

    Args:
        request: MaskingRequest with file path and classification

    Returns:
        MaskingResponse with output path and statistics
    """
    # Validate input file exists
    if not os.path.exists(request.input_path):
        raise HTTPException(status_code=404, detail=f"Input file not found: {request.input_path}")

    # Read CSV
    try:
        df = pd.read_csv(request.input_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

    rows_processed = len(df)
    techniques_applied = {}

    classification = request.classification

    # Step 0: Extract names BEFORE suppression for text scrubbing
    names_to_scrub = set()
    if classification.recommended_techniques:
        for col, technique in classification.recommended_techniques.items():
            if technique.upper() == "SUPPRESS" and col in df.columns:
                # Extract names from columns being suppressed (like 'name' column)
                names_to_scrub.update(TextScrubber.extract_names_from_column(df, col))

    # Step 0.5: Scrub PII from sensitive text columns (before other operations)
    text_columns_to_scrub = []
    if classification.sensitive_attributes:
        for col in classification.sensitive_attributes:
            # Scrub text columns (likely to contain free text with embedded PII)
            if col in df.columns and df[col].dtype == 'object':
                text_columns_to_scrub.append(col)

    if text_columns_to_scrub:
        text_scrubber = TextScrubber(
            text_columns=text_columns_to_scrub,
            names_to_scrub=names_to_scrub,
            replacement="[REDACTED]"
        )
        scrubbed = text_scrubber.get_scrubbed_columns(df)
        df = text_scrubber.apply(df)
        for col in scrubbed:
            techniques_applied[col] = "TEXT_SCRUBBED"

    # Step 1: Suppress columns - USE recommended_techniques as source of truth
    # This ensures correct behavior even if AI categorizes a column in the wrong array
    columns_to_suppress = []

    if classification.recommended_techniques:
        # Primary: Use recommended_techniques to determine what to suppress
        for col, technique in classification.recommended_techniques.items():
            if technique.upper() == "SUPPRESS" and col in df.columns:
                columns_to_suppress.append(col)
    else:
        # Fallback: If no recommended_techniques, use direct_identifiers array
        columns_to_suppress = list(classification.direct_identifiers) if classification.direct_identifiers else []

    if columns_to_suppress:
        suppressor = Suppressor(columns_to_suppress)
        suppressed = suppressor.get_suppressed_columns(df)
        df = suppressor.apply(df)
        for col in suppressed:
            techniques_applied[col] = "SUPPRESSED"

    # Step 2: Date shift - USE recommended_techniques as source of truth
    columns_to_date_shift = []

    if classification.recommended_techniques:
        # Primary: Use recommended_techniques to determine what to date shift
        for col, technique in classification.recommended_techniques.items():
            if technique.upper() == "DATE_SHIFT" and col in df.columns:
                columns_to_date_shift.append(col)
    else:
        # Fallback: If no recommended_techniques, use date_columns array
        columns_to_date_shift = list(classification.date_columns) if classification.date_columns else []

    if columns_to_date_shift:
        date_shifter = DateShifter(
            date_columns=columns_to_date_shift,
            salt=request.salt,
            min_days=-365,
            max_days=365
        )
        shifted = date_shifter.get_shifted_columns(df)
        df = date_shifter.apply(df)
        for col in shifted:
            techniques_applied[col] = "DATE_SHIFTED"

    # Step 3: Generalize - USE recommended_techniques as source of truth
    columns_to_generalize = []

    if classification.recommended_techniques:
        # Primary: Use recommended_techniques to determine what to generalize
        for col, technique in classification.recommended_techniques.items():
            if technique.upper() == "GENERALIZE" and col in df.columns:
                columns_to_generalize.append(col)
    else:
        # Fallback: If no recommended_techniques, use quasi_identifiers array
        columns_to_generalize = list(classification.quasi_identifiers) if classification.quasi_identifiers else []

    if columns_to_generalize:
        gen_config = classification.generalization_config
        generalizer = Generalizer(
            quasi_identifiers=columns_to_generalize,
            age_level=gen_config.age_level,
            location_level=gen_config.location_level,
            date_level=gen_config.date_level
        )
        generalized = generalizer.get_generalized_columns(df)
        df = generalizer.apply(df)
        for col in generalized:
            techniques_applied[col] = "GENERALIZED"

    # Step 4: Pseudonymize - USE recommended_techniques as source of truth
    columns_to_pseudonymize = []

    if classification.recommended_techniques:
        # Primary: Use recommended_techniques to determine what to pseudonymize
        for col, technique in classification.recommended_techniques.items():
            if technique.upper() == "PSEUDONYMIZE" and col in df.columns:
                columns_to_pseudonymize.append(col)
    else:
        # Fallback: If no recommended_techniques, use linkage_identifiers array
        columns_to_pseudonymize = list(classification.linkage_identifiers) if classification.linkage_identifiers else []

    if columns_to_pseudonymize:
        pseudonymizer = Pseudonymizer(
            linkage_columns=columns_to_pseudonymize,
            salt=request.salt,
            hash_length=12
        )
        pseudonymized = pseudonymizer.get_pseudonymized_columns(df)
        df = pseudonymizer.apply(df)
        for col in pseudonymized:
            techniques_applied[col] = "PSEUDONYMIZED"

    # Mark sensitive attributes as kept
    for col in classification.sensitive_attributes:
        if col in df.columns and col not in techniques_applied:
            techniques_applied[col] = "KEPT"

    # Ensure staging directory exists
    os.makedirs(STAGING_PATH, exist_ok=True)

    # Write output
    output_filename = f"{request.job_id}_masked.csv"
    output_path = os.path.join(STAGING_PATH, output_filename)

    try:
        df.to_csv(output_path, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write output: {str(e)}")

    columns_masked = len(techniques_applied)

    return MaskingResponse(
        output_path=output_path,
        techniques_applied=techniques_applied,
        rows_processed=rows_processed,
        columns_masked=columns_masked
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "masking-service"}
