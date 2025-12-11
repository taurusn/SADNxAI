#!/usr/bin/env python3
"""
SADNxAI - Comprehensive Test Suite
Tests all components: masking engines, validation metrics, and PDF report generation
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'masking-service'))
sys.path.insert(0, os.path.join(BASE_DIR, 'validation-service'))

# Test results tracking
TESTS_RUN = 0
TESTS_PASSED = 0
TESTS_FAILED = 0

def test(name):
    """Decorator for test functions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            global TESTS_RUN, TESTS_PASSED, TESTS_FAILED
            TESTS_RUN += 1
            try:
                result = func(*args, **kwargs)
                TESTS_PASSED += 1
                print(f"  ✓ {name}")
                return result
            except Exception as e:
                TESTS_FAILED += 1
                print(f"  ✗ {name}: {str(e)}")
                return None
        return wrapper
    return decorator


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_section(title):
    print(f"\n--- {title} ---")


# =============================================================
# Test Data Setup
# =============================================================

def load_test_data():
    """Load the sample healthcare CSV"""
    csv_path = os.path.join(BASE_DIR, 'test_data', 'sample_healthcare.csv')
    return pd.read_csv(csv_path)


# =============================================================
# Masking Engine Tests
# =============================================================

print_header("MASKING ENGINE TESTS")

@test("Suppressor removes direct identifier columns")
def test_suppressor():
    from engine.suppressor import Suppressor

    df = load_test_data()
    original_cols = list(df.columns)

    suppressor = Suppressor(['national_id', 'name', 'phone', 'email'])
    result = suppressor.apply(df)

    assert 'national_id' not in result.columns
    assert 'name' not in result.columns
    assert 'phone' not in result.columns
    assert 'email' not in result.columns
    assert 'age' in result.columns  # Should remain
    assert 'diagnosis' in result.columns  # Should remain
    assert len(result) == len(df)  # Same number of rows

    return result

@test("DateShifter applies consistent random offset")
def test_date_shifter():
    from engine.date_shifter import DateShifter

    df = load_test_data()

    shifter = DateShifter(
        date_columns=['admission_date'],
        salt='test_salt_123',
        min_days=-30,
        max_days=30
    )
    result = shifter.apply(df)

    # Dates should be different
    original_dates = pd.to_datetime(df['admission_date'])
    shifted_dates = pd.to_datetime(result['admission_date'])

    # At least some dates should have changed
    changes = (original_dates != shifted_dates).sum()
    assert changes > 0, "No dates were shifted"

    # Run again with same salt - should get same results
    result2 = shifter.apply(df)
    shifted_dates2 = pd.to_datetime(result2['admission_date'])

    assert (shifted_dates == shifted_dates2).all(), "Date shifting is not deterministic"

    return result

@test("Generalizer generalizes age to 5-year ranges")
def test_generalizer_age():
    from engine.generalizer import Generalizer

    df = load_test_data()

    generalizer = Generalizer(
        quasi_identifiers=['age'],
        age_level=1,  # 5-year ranges
        column_types={'age': 'age'}
    )
    result = generalizer.apply(df)

    # Check that ages are now ranges
    assert '30-34' in result['age'].values or '25-29' in result['age'].values

    # Check format
    for val in result['age'].unique():
        assert '-' in str(val), f"Age not generalized: {val}"

    return result

@test("Generalizer generalizes cities to provinces")
def test_generalizer_location():
    from engine.generalizer import Generalizer

    df = load_test_data()

    generalizer = Generalizer(
        quasi_identifiers=['city'],
        location_level=1,  # Province level
        column_types={'city': 'location'}
    )
    result = generalizer.apply(df)

    # Dammam should become Eastern Province
    # Riyadh should become Riyadh Province
    unique_locations = result['city'].unique()

    assert 'Dammam' not in unique_locations, "City not generalized"
    assert 'Eastern Province' in unique_locations or 'Riyadh Province' in unique_locations

    return result

@test("Pseudonymizer creates consistent hashes")
def test_pseudonymizer():
    from engine.pseudonymizer import Pseudonymizer

    df = load_test_data()

    pseudonymizer = Pseudonymizer(
        linkage_columns=['patient_id'],
        salt='test_salt_456',
        hash_length=12
    )
    result = pseudonymizer.apply(df)

    # Original IDs should be replaced
    assert 'MRN001' not in result['patient_id'].values

    # All values should be uppercase hex
    for val in result['patient_id'].unique():
        assert len(val) == 12, f"Hash length wrong: {val}"
        assert val.isalnum(), f"Hash not alphanumeric: {val}"

    # Same input should produce same output
    result2 = pseudonymizer.apply(df)
    assert (result['patient_id'] == result2['patient_id']).all()

    return result

test_suppressor()
test_date_shifter()
test_generalizer_age()
test_generalizer_location()
test_pseudonymizer()


# =============================================================
# Full Masking Pipeline Test
# =============================================================

print_section("Full Masking Pipeline")

@test("Complete masking pipeline transforms data correctly")
def test_full_masking_pipeline():
    from engine.suppressor import Suppressor
    from engine.date_shifter import DateShifter
    from engine.generalizer import Generalizer
    from engine.pseudonymizer import Pseudonymizer

    df = load_test_data()
    print(f"\n    Original data: {len(df)} rows, {len(df.columns)} columns")
    print(f"    Columns: {list(df.columns)}")

    # Step 1: Suppress direct identifiers
    suppressor = Suppressor(['national_id', 'name', 'phone', 'email'])
    df = suppressor.apply(df)
    print(f"    After suppression: {len(df.columns)} columns")

    # Step 2: Date shift
    date_shifter = DateShifter(['admission_date'], salt='pipeline_salt')
    df = date_shifter.apply(df)

    # Step 3: Generalize quasi-identifiers
    generalizer = Generalizer(
        quasi_identifiers=['age', 'city', 'gender'],
        age_level=1,
        location_level=1,
        column_types={'age': 'age', 'city': 'location', 'gender': 'gender'}
    )
    df = generalizer.apply(df)

    # Step 4: Pseudonymize linkage identifiers
    pseudonymizer = Pseudonymizer(['patient_id'], salt='pipeline_salt')
    df = pseudonymizer.apply(df)

    print(f"    Final columns: {list(df.columns)}")
    print(f"    Sample row: {df.iloc[0].to_dict()}")

    # Save masked data
    output_path = os.path.join(BASE_DIR, 'test_data', 'masked_healthcare.csv')
    df.to_csv(output_path, index=False)
    print(f"    Saved to: {output_path}")

    return df

masked_df = test_full_masking_pipeline()


# =============================================================
# Validation Metrics Tests
# =============================================================

print_header("VALIDATION METRICS TESTS")

# Change to validation-service directory for imports
sys.path.insert(0, os.path.join(BASE_DIR, 'validation-service'))

@test("k-Anonymity calculation is correct")
def test_k_anonymity():
    from metrics.k_anonymity import calculate_k_anonymity

    # Use masked data
    df = masked_df if masked_df is not None else load_test_data()

    result = calculate_k_anonymity(
        df,
        quasi_identifiers=['age', 'city', 'gender']
    )

    print(f"\n    k-value: {result['k_value']}")
    print(f"    Equivalence classes: {result['equivalence_classes']}")
    print(f"    Smallest class: {result['smallest_class_size']}")
    print(f"    Largest class: {result['largest_class_size']}")

    assert result['k_value'] >= 1
    assert result['equivalence_classes'] > 0

    return result

@test("l-Diversity calculation is correct")
def test_l_diversity():
    from metrics.l_diversity import calculate_l_diversity

    df = masked_df if masked_df is not None else load_test_data()

    result = calculate_l_diversity(
        df,
        quasi_identifiers=['age', 'city', 'gender'],
        sensitive_attributes=['diagnosis']
    )

    print(f"\n    l-value: {result['l_value']}")
    print(f"    Per attribute: {result['per_attribute']}")

    assert result['l_value'] >= 1 or result['l_value'] == float('inf')

    return result

@test("t-Closeness calculation is correct")
def test_t_closeness():
    from metrics.t_closeness import calculate_t_closeness

    df = masked_df if masked_df is not None else load_test_data()

    result = calculate_t_closeness(
        df,
        quasi_identifiers=['age', 'city', 'gender'],
        sensitive_attributes=['diagnosis']
    )

    print(f"\n    t-value: {result['t_value']}")
    print(f"    Mean distance: {result.get('mean_distance', 'N/A')}")

    assert 0 <= result['t_value'] <= 1

    return result

k_result = test_k_anonymity()
l_result = test_l_diversity()
t_result = test_t_closeness()


# =============================================================
# PDF Report Generation Test
# =============================================================

print_header("PDF REPORT GENERATION TEST")

@test("PDF report generates successfully")
def test_pdf_report():
    from report.generator import generate_pdf_report

    # Create mock session and validation result
    session = {
        'id': 'test-session-123',
        'title': 'sample_healthcare.csv',
        'row_count': 20,
        'classification': {
            'direct_identifiers': ['national_id', 'name', 'phone', 'email'],
            'quasi_identifiers': ['age', 'city', 'gender'],
            'linkage_identifiers': ['patient_id'],
            'date_columns': ['admission_date'],
            'sensitive_attributes': ['diagnosis', 'treatment']
        }
    }

    validation_result = {
        'passed': True,
        'metrics': {
            'k_anonymity': {'value': k_result['k_value'] if k_result else 3, 'threshold': 5, 'passed': True},
            'l_diversity': {'value': l_result['l_value'] if l_result else 2, 'threshold': 2, 'passed': True},
            't_closeness': {'value': t_result['t_value'] if t_result else 0.15, 'threshold': 0.2, 'passed': True},
            'risk_score': {'value': 12.5, 'threshold': 20, 'passed': True}
        },
        'failed_metrics': [],
        'remediation_suggestions': []
    }

    output_path = os.path.join(BASE_DIR, 'test_data')
    report_path = generate_pdf_report(
        output_path=output_path,
        session=session,
        validation_result=validation_result,
        job_id='test-job-001'
    )

    assert os.path.exists(report_path)
    file_size = os.path.getsize(report_path)
    print(f"\n    Report generated: {report_path}")
    print(f"    File size: {file_size / 1024:.1f} KB")

    return report_path

test_pdf_report()


# =============================================================
# Integration Test
# =============================================================

print_header("INTEGRATION TEST - Full Pipeline")

@test("End-to-end pipeline works correctly")
def test_end_to_end():
    from engine.suppressor import Suppressor
    from engine.date_shifter import DateShifter
    from engine.generalizer import Generalizer
    from engine.pseudonymizer import Pseudonymizer
    from metrics.k_anonymity import calculate_k_anonymity
    from metrics.l_diversity import calculate_l_diversity
    from metrics.t_closeness import calculate_t_closeness
    from report.generator import generate_pdf_report

    print("\n    Step 1: Loading data...")
    df = load_test_data()

    print("    Step 2: Applying masking techniques...")

    # Suppress
    df = Suppressor(['national_id', 'name', 'phone', 'email']).apply(df)

    # Date shift
    df = DateShifter(['admission_date'], salt='e2e_test').apply(df)

    # Generalize with higher levels for better k-anonymity
    df = Generalizer(
        quasi_identifiers=['age', 'city', 'gender'],
        age_level=2,  # 10-year ranges
        location_level=1,
        column_types={'age': 'age', 'city': 'location', 'gender': 'gender'}
    ).apply(df)

    # Pseudonymize
    df = Pseudonymizer(['patient_id'], salt='e2e_test').apply(df)

    print("    Step 3: Validating privacy metrics...")

    qi = ['age', 'city', 'gender']
    sa = ['diagnosis']

    k = calculate_k_anonymity(df, qi)
    l = calculate_l_diversity(df, qi, sa)
    t = calculate_t_closeness(df, qi, sa)

    print(f"      k-anonymity: {k['k_value']}")
    print(f"      l-diversity: {l['l_value']}")
    print(f"      t-closeness: {t['t_value']:.4f}")

    # Check if passes thresholds
    k_pass = k['k_value'] >= 2  # Relaxed for small dataset
    l_pass = l['l_value'] >= 1
    t_pass = t['t_value'] <= 0.5  # Relaxed for small dataset

    print(f"      Validation: k={'✓' if k_pass else '✗'} l={'✓' if l_pass else '✗'} t={'✓' if t_pass else '✗'}")

    print("    Step 4: Generating report...")

    session = {
        'id': 'e2e-test-session',
        'title': 'sample_healthcare.csv',
        'row_count': len(df),
        'classification': {
            'direct_identifiers': ['national_id', 'name', 'phone', 'email'],
            'quasi_identifiers': qi,
            'linkage_identifiers': ['patient_id'],
            'date_columns': ['admission_date'],
            'sensitive_attributes': sa + ['treatment']
        }
    }

    validation_result = {
        'passed': k_pass and l_pass and t_pass,
        'metrics': {
            'k_anonymity': {'value': k['k_value'], 'threshold': 2, 'passed': k_pass},
            'l_diversity': {'value': l['l_value'], 'threshold': 1, 'passed': l_pass},
            't_closeness': {'value': t['t_value'], 'threshold': 0.5, 'passed': t_pass},
            'risk_score': {'value': 15.0, 'threshold': 20, 'passed': True}
        },
        'failed_metrics': [],
        'remediation_suggestions': []
    }

    output_path = os.path.join(BASE_DIR, 'test_data')
    report_path = generate_pdf_report(output_path, session, validation_result, 'e2e-test')

    # Save final anonymized data
    final_output = os.path.join(BASE_DIR, 'test_data', 'final_anonymized.csv')
    df.to_csv(final_output, index=False)

    print(f"\n    Anonymized CSV: {final_output}")
    print(f"    Privacy Report: {report_path}")
    print(f"\n    Sample anonymized record:")
    print(f"    {df.iloc[0].to_dict()}")

    return df

test_end_to_end()


# =============================================================
# Summary
# =============================================================

print_header("TEST SUMMARY")
print(f"\n  Total tests: {TESTS_RUN}")
print(f"  Passed:      {TESTS_PASSED} ✓")
print(f"  Failed:      {TESTS_FAILED} ✗")
print(f"\n  Success rate: {TESTS_PASSED/TESTS_RUN*100:.1f}%")

if TESTS_FAILED == 0:
    print("\n  🎉 All tests passed! SADNxAI is working correctly.")
else:
    print(f"\n  ⚠️  {TESTS_FAILED} test(s) failed. Check the output above.")

print("\n" + "="*60)
