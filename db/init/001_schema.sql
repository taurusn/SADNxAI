-- ============================================
-- SADNxAI Database Schema
-- PostgreSQL 15+
-- ============================================

-- ============================================
-- LOOKUP TABLES (Seeded once, rarely changed)
-- ============================================

-- Masking techniques
CREATE TABLE techniques (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Classification types with linked technique
CREATE TABLE classification_types (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    technique_id VARCHAR(50) NOT NULL REFERENCES techniques(id),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Regulations (PDPL articles, SAMA requirements)
CREATE TABLE regulations (
    id VARCHAR(50) PRIMARY KEY,
    source VARCHAR(20) NOT NULL,
    article_number VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    full_text TEXT NOT NULL,
    summary TEXT,
    applies_to TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Which regulations justify each technique (many-to-many)
CREATE TABLE technique_regulations (
    id SERIAL PRIMARY KEY,
    technique_id VARCHAR(50) NOT NULL REFERENCES techniques(id),
    regulation_id VARCHAR(50) NOT NULL REFERENCES regulations(id),
    justification TEXT NOT NULL,
    rationale TEXT,
    priority INT DEFAULT 1,
    UNIQUE(technique_id, regulation_id)
);

-- Validation metric definitions
CREATE TABLE validations (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    default_minimum FLOAT,
    default_target FLOAT,
    is_lower_better BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Saudi data patterns for auto-detection
CREATE TABLE saudi_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(50) NOT NULL,
    regex_pattern VARCHAR(255) NOT NULL,
    classification_type_id VARCHAR(50) REFERENCES classification_types(id),
    regulation_id VARCHAR(50) REFERENCES regulations(id),
    description TEXT,
    UNIQUE(pattern_name)
);

-- ============================================
-- DATA TABLES (Created per job)
-- ============================================

-- Jobs (main job/session data)
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL DEFAULT 'New Job',
    status VARCHAR(50) NOT NULL DEFAULT 'idle',
    file_path VARCHAR(500),
    columns JSONB,
    row_count INT,
    sample_data JSONB,
    thresholds JSONB,
    masked_path VARCHAR(500),
    report_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Per-column classifications for each job
CREATE TABLE classifications_on_jobs (
    id SERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    classification_type_id VARCHAR(50) NOT NULL REFERENCES classification_types(id),
    reasoning TEXT,
    generalization_level INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(job_id, column_name)
);

-- Regulation citations for each classification
CREATE TABLE classification_regulations (
    id SERIAL PRIMARY KEY,
    classification_on_job_id INT NOT NULL REFERENCES classifications_on_jobs(id) ON DELETE CASCADE,
    regulation_id VARCHAR(50) NOT NULL REFERENCES regulations(id),
    relevance TEXT,
    UNIQUE(classification_on_job_id, regulation_id)
);

-- Validation results per job
CREATE TABLE validation_on_jobs (
    id SERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    validation_id VARCHAR(50) NOT NULL REFERENCES validations(id),
    value FLOAT NOT NULL,
    threshold_used FLOAT,
    passed BOOLEAN NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(job_id, validation_id)
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(created_at DESC);
CREATE INDEX idx_jobs_updated ON jobs(updated_at DESC);
CREATE INDEX idx_classifications_job ON classifications_on_jobs(job_id);
CREATE INDEX idx_classification_regs ON classification_regulations(classification_on_job_id);
CREATE INDEX idx_validation_job ON validation_on_jobs(job_id);
CREATE INDEX idx_regulations_source ON regulations(source);
CREATE INDEX idx_technique_regs_tech ON technique_regulations(technique_id);
CREATE INDEX idx_patterns_classification ON saudi_patterns(classification_type_id);

-- Full-text search on regulations
CREATE INDEX idx_regulations_fts ON regulations
    USING GIN(to_tsvector('english', full_text || ' ' || title));
