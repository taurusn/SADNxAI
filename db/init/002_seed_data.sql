-- ============================================
-- SADNxAI Seed Data
-- Lookup tables for techniques, classifications, regulations
-- ============================================

-- ============================================
-- TECHNIQUES
-- ============================================
INSERT INTO techniques (id, name, description) VALUES
('SUPPRESS', 'Suppress', 'Complete removal of direct identifiers'),
('GENERALIZE', 'Generalize', 'Replace specific values with ranges or categories'),
('PSEUDONYMIZE', 'Pseudonymize', 'Replace with consistent hash (HMAC-SHA256)'),
('DATE_SHIFT', 'Date Shift', 'Random offset preserving intervals'),
('KEEP', 'Keep', 'Preserve for analysis (sensitive attributes)'),
('TEXT_SCRUB', 'Text Scrub', 'PII detection and redaction in free text');

-- ============================================
-- CLASSIFICATION TYPES (linked to techniques)
-- ============================================
INSERT INTO classification_types (id, name, technique_id, description) VALUES
('direct_identifier', 'Direct Identifier', 'SUPPRESS', 'Data that directly identifies an individual (name, ID, phone, email, IBAN)'),
('quasi_identifier', 'Quasi Identifier', 'GENERALIZE', 'Data that could identify when combined (age, city, gender, occupation)'),
('linkage_identifier', 'Linkage Identifier', 'PSEUDONYMIZE', 'IDs used for record linking across datasets (customer_id, account_id)'),
('date_column', 'Date Column', 'DATE_SHIFT', 'Date and timestamp fields'),
('sensitive_attribute', 'Sensitive Attribute', 'KEEP', 'Analysis target data that must be preserved (amount, fraud_flag, transaction_type)');

-- ============================================
-- REGULATIONS (PDPL - Personal Data Protection Law)
-- ============================================
INSERT INTO regulations (id, source, article_number, title, full_text, summary, applies_to) VALUES
('PDPL-Art-5', 'PDPL', '5', 'Sensitive Personal Data',
 'Sensitive personal data includes data revealing racial or ethnic origin, religious or political beliefs, health data, genetic data, biometric data, financial data, credit data, and criminal records. Processing such data requires explicit consent and additional safeguards.',
 'Defines sensitive data categories requiring extra protection',
 ARRAY['sensitive_attribute', 'KEEP', 'financial']),

('PDPL-Art-10', 'PDPL', '10', 'Consent Requirements',
 'Processing personal data requires consent from the data subject, which must be explicit, informed, freely given, and specific to the processing purpose. Consent may be withdrawn at any time.',
 'Explicit consent required for processing personal data',
 ARRAY['direct_identifier', 'SUPPRESS', 'consent']),

('PDPL-Art-11', 'PDPL', '11', 'Data Minimization',
 'Personal data must be limited to the minimum necessary for the purposes for which it is processed. Controllers must not collect or retain data beyond what is required for the specified purpose.',
 'Collect and retain only minimum necessary data',
 ARRAY['SUPPRESS', 'direct_identifier', 'GENERALIZE', 'data_retention']),

('PDPL-Art-15', 'PDPL', '15', 'Disclosure Restrictions',
 'Personal data may only be disclosed to third parties with the explicit consent of the data subject, or in an anonymized form that prevents identification of the individual.',
 'Disclosure requires consent OR anonymization',
 ARRAY['SUPPRESS', 'GENERALIZE', 'disclosure', 'third_party']),

('PDPL-Art-17', 'PDPL', '17', 'Data Quality',
 'Personal data must be accurate, complete, and kept up to date where necessary for the purposes for which it is processed. Inaccurate data must be corrected or deleted.',
 'Maintain data accuracy and quality',
 ARRAY['quasi_identifier', 'GENERALIZE', 'accuracy']),

('PDPL-Art-18', 'PDPL', '18', 'Storage Limitation',
 'Personal data must not be stored longer than necessary for the specified purpose. When data is no longer needed, it must be securely deleted or anonymized.',
 'Delete or anonymize data when no longer needed',
 ARRAY['SUPPRESS', 'retention', 'deletion']),

('PDPL-Art-19', 'PDPL', '19', 'Technical and Organizational Measures',
 'Controllers must implement appropriate technical and organizational measures to protect personal data against unauthorized access, disclosure, alteration, or destruction. This includes encryption, pseudonymization, and access controls.',
 'Implement technical safeguards for data protection',
 ARRAY['PSEUDONYMIZE', 'linkage_identifier', 'technical', 'security']),

('PDPL-Art-23', 'PDPL', '23', 'Security Breach Notification',
 'In case of a personal data breach that poses risk to the rights and freedoms of data subjects, the controller must notify the competent authority within 72 hours and affected individuals without undue delay.',
 'Breach notification required within 72 hours',
 ARRAY['security', 'breach', 'notification']),

('PDPL-Art-24', 'PDPL', '24', 'Credit and Financial Data',
 'Processing of credit data and financial records requires explicit consent and is subject to additional safeguards. Such data may only be processed for legitimate purposes related to credit assessment or fraud prevention.',
 'Extra protection required for credit and financial data',
 ARRAY['sensitive_attribute', 'financial', 'credit']),

('PDPL-Art-28', 'PDPL', '28', 'National ID Protection',
 'National identification numbers and government-issued identifiers require special protection and may only be processed when strictly necessary and with appropriate safeguards.',
 'Special protection for national IDs',
 ARRAY['direct_identifier', 'SUPPRESS', 'national_id']),

('PDPL-Art-29', 'PDPL', '29', 'Cross-Border Data Transfers',
 'Transfer of personal data outside Saudi Arabia requires adequate protection level in the destination country, binding corporate rules, or explicit consent of the data subject.',
 'Cross-border transfers need adequate protection',
 ARRAY['transfer', 'international', 'adequacy']),

('PDPL-Art-31', 'PDPL', '31', 'Penalties and Enforcement',
 'Violations of the PDPL are subject to administrative fines up to 5 million SAR, criminal penalties including imprisonment, and civil liability for damages caused to data subjects.',
 'Significant penalties for non-compliance',
 ARRAY['compliance', 'penalties', 'enforcement']);

-- ============================================
-- REGULATIONS (SAMA - Saudi Arabian Monetary Authority)
-- ============================================
INSERT INTO regulations (id, source, article_number, title, full_text, summary, applies_to) VALUES
('SAMA-2.6.1', 'SAMA', '2.6.1', 'Data Classification Requirements',
 'Financial institutions must classify all data based on sensitivity levels (public, internal, confidential, restricted) and implement appropriate controls for each classification level.',
 'Classify and protect data based on sensitivity',
 ARRAY['classification', 'direct_identifier', 'quasi_identifier', 'sensitivity']),

('SAMA-2.6.2', 'SAMA', '2.6.2', 'Data Security and Localization',
 'Personal and financial data must be secured in Saudi-based facilities. Payment card data requires PCI DSS compliance. Strong encryption must be used for data at rest and in transit.',
 'Saudi-based storage with PCI DSS compliance',
 ARRAY['security', 'storage', 'SUPPRESS', 'localization', 'encryption']),

('SAMA-2.6.3', 'SAMA', '2.6.3', 'Third-Party Data Sharing',
 'Sharing customer data with third parties requires explicit customer consent OR the data must be anonymized to prevent identification. All third-party sharing must be logged and auditable.',
 'Third-party sharing needs consent or anonymization',
 ARRAY['sharing', 'SUPPRESS', 'GENERALIZE', 'third_party', 'audit']),

('SAMA-OB', 'SAMA', 'Open Banking', 'Open Banking Framework',
 'Third Party Providers (TPPs) may access customer data only with explicit consent. Data sharing must be secure, use standard APIs, and maintain full audit trails. Customer can revoke consent at any time.',
 'Secure and auditable data sharing for open banking',
 ARRAY['api', 'sharing', 'PSEUDONYMIZE', 'consent', 'tpp']),

('SAMA-BCT', 'SAMA', 'BCT/15631', 'Cybersecurity Framework',
 'Financial institutions must implement comprehensive cybersecurity controls including data loss prevention, encryption, access management, and incident response capabilities.',
 'Comprehensive cybersecurity controls mandatory',
 ARRAY['security', 'technical', 'dlp', 'encryption']);

-- ============================================
-- TECHNIQUE-REGULATION MAPPINGS
-- ============================================

-- SUPPRESS justifications
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
('SUPPRESS', 'PDPL-Art-11',
 'Direct identifiers must be suppressed per data minimization principle',
 'Names, national IDs, phone numbers, and email addresses exceed the minimum necessary for most analytics and must be removed to comply with data minimization requirements.', 1),
('SUPPRESS', 'PDPL-Art-15',
 'Suppression ensures disclosure does not enable identification',
 'Complete removal of direct identifiers is the most effective anonymization technique, ensuring that disclosed data cannot be used to identify individuals.', 2),
('SUPPRESS', 'PDPL-Art-28',
 'National IDs require special protection through complete removal',
 'Government-issued identifiers like National ID and Iqama numbers are high-risk identifiers that should be suppressed in analytical datasets.', 3),
('SUPPRESS', 'SAMA-2.6.2',
 'Sensitive identifiers must be removed before processing outside secure facilities',
 'SAMA requires personal data to be secured in Saudi facilities. Suppression enables compliant data processing and sharing.', 4),
('SUPPRESS', 'SAMA-2.6.3',
 'Suppression enables compliant third-party data sharing',
 'When customer consent is not available, suppressing direct identifiers allows data to be shared with third parties for analytics.', 5);

-- GENERALIZE justifications
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
('GENERALIZE', 'PDPL-Art-11',
 'Generalization reduces data to minimum necessary granularity',
 'Age ranges (e.g., 25-30) and location hierarchies (e.g., city to region) preserve analytical utility while reducing precision to minimum necessary.', 1),
('GENERALIZE', 'PDPL-Art-17',
 'Generalized data maintains accuracy at aggregate level',
 'Ranges and categories remain accurate representations of the underlying data while significantly reducing re-identification risk.', 2),
('GENERALIZE', 'PDPL-Art-15',
 'Generalization supports compliant disclosure',
 'Generalized quasi-identifiers can be disclosed without consent when combined generalization achieves sufficient anonymization.', 3),
('GENERALIZE', 'SAMA-2.6.3',
 'Generalization enables compliant third-party sharing',
 'Generalized demographic and location data can be shared with third parties while maintaining customer privacy.', 4);

-- PSEUDONYMIZE justifications
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
('PSEUDONYMIZE', 'PDPL-Art-19',
 'Pseudonymization is a recognized technical protection measure',
 'HMAC-based pseudonyms using session-specific salts enable record linking across datasets without exposing original identifiers.', 1),
('PSEUDONYMIZE', 'SAMA-OB',
 'Pseudonymous identifiers support secure open banking data flows',
 'TPPs can work with pseudonymous customer and account IDs for fraud detection and analytics without accessing real identifiers.', 2),
('PSEUDONYMIZE', 'SAMA-2.6.2',
 'Pseudonymization provides technical security for linkage IDs',
 'Consistent hashing allows internal record linking while preventing identifier exposure in case of data breach.', 3);

-- DATE_SHIFT justifications
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
('DATE_SHIFT', 'PDPL-Art-11',
 'Date shifting minimizes temporal precision while preserving patterns',
 'Random offsets (typically +/- 365 days) preserve relative timing between events (important for fraud detection) while preventing exact date matching.', 1),
('DATE_SHIFT', 'PDPL-Art-15',
 'Date shifting supports anonymous disclosure of temporal data',
 'Shifted dates cannot be matched to known events or records, enabling compliant disclosure of time-series data.', 2);

-- KEEP justifications
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
('KEEP', 'PDPL-Art-5',
 'Sensitive attributes preserved for legitimate analysis purposes',
 'Transaction amounts, fraud flags, and other sensitive attributes are the analysis targets and must be preserved. They are protected through anonymization of identifiers.', 1),
('KEEP', 'PDPL-Art-24',
 'Financial data retained for credit scoring and fraud detection',
 'Legitimate purposes like fraud detection and credit assessment require preservation of financial attributes in the anonymized dataset.', 2),
('KEEP', 'SAMA-2.6.1',
 'Sensitive attributes classified and protected appropriately',
 'While preserved for analysis, sensitive attributes are protected through suppression and generalization of associated identifiers.', 3);

-- ============================================
-- VALIDATIONS (Privacy metric definitions)
-- ============================================
INSERT INTO validations (id, name, description, default_minimum, default_target, is_lower_better) VALUES
('k_anonymity', 'K-Anonymity',
 'Each record is indistinguishable from at least k-1 other records on quasi-identifier attributes. Higher k means better privacy.',
 5, 10, FALSE),
('l_diversity', 'L-Diversity',
 'Each equivalence class (group of k-anonymous records) contains at least l distinct values of sensitive attributes. Prevents attribute disclosure.',
 2, 3, FALSE),
('t_closeness', 'T-Closeness',
 'The distribution of sensitive attribute values in each equivalence class is close to the overall distribution. Measured by Earth Mover''s Distance. Lower is better.',
 0.2, 0.15, TRUE),
('risk_score', 'Risk Score',
 'Composite re-identification risk percentage based on uniqueness of quasi-identifier combinations. Lower is better.',
 20, 10, TRUE);

-- ============================================
-- SAUDI PATTERNS (Auto-detection patterns)
-- ============================================
INSERT INTO saudi_patterns (pattern_name, regex_pattern, classification_type_id, regulation_id, description) VALUES
('national_id', '^1[0-9]{9}$', 'direct_identifier', 'PDPL-Art-28',
 'Saudi National ID - 10 digits starting with 1'),
('iqama', '^2[0-9]{9}$', 'direct_identifier', 'PDPL-Art-28',
 'Resident ID (Iqama) - 10 digits starting with 2'),
('phone_966', '^(\+966|00966|966)[0-9]{9}$', 'direct_identifier', 'PDPL-Art-11',
 'Saudi phone number with country code (+966)'),
('phone_05', '^05[0-9]{8}$', 'direct_identifier', 'PDPL-Art-11',
 'Saudi mobile number starting with 05'),
('iban', '^SA[0-9]{22}$', 'direct_identifier', 'SAMA-2.6.2',
 'Saudi IBAN - SA followed by 22 digits'),
('card_pan', '^[0-9]{16}$', 'direct_identifier', 'SAMA-2.6.2',
 'Payment card number - 16 digits (requires context validation)'),
('email', '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 'direct_identifier', 'PDPL-Art-11',
 'Email address pattern');
