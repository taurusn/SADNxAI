# Implementation Plan: Regulation Database & Prompt Optimization

## Overview

This plan enhances SADNxAI with:
1. **PostgreSQL Database** - Normalized schema for jobs, regulations, classifications, validations
2. **Redis** - Keep for session caching and chat messages (fast access)
3. **query_regulations Tool** - LLM tool to fetch and cite regulations
4. **State-Based Prompts** - Optimized prompts per session state
5. **Enhanced Justifications** - Store regulation references with classifications

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Docker Compose Network                         │
├─────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│  Frontend   │ Chat Service │   Masking    │  Validation  │   Ollama    │
│  (Next.js)  │  (FastAPI)   │   Service    │   Service    │   (GPU)     │
│   :3000     │    :8000     │    :8001     │    :8002     │   :11434    │
└──────┬──────┴──────┬───────┴──────┬───────┴──────┬───────┴─────────────┘
       │             │              │              │
       │      ┌──────┴──────┐       │              │
       │      │             │       │              │
       │      ▼             ▼       │              │
       │  ┌───────┐   ┌──────────┐  │              │
       │  │ Redis │   │ PostgreSQL│  │              │
       │  │ :6379 │   │  :5432   │  │              │
       │  └───────┘   └──────────┘  │              │
       │      │             │       │              │
       │      │   Messages  │  Jobs, Regulations   │
       │      │   Cache     │  Classifications     │
       │      │             │  Validations         │
       └──────┴─────────────┴───────┴──────────────┘
```

### Data Storage Strategy

| Data Type | Storage | Reason |
|-----------|---------|--------|
| Chat messages | Redis (JSON in session) | Fast access, ephemeral |
| Session cache | Redis | Quick lookups, TTL support |
| Jobs | PostgreSQL | Persistence, querying, audit trail |
| Regulations | PostgreSQL | Structured queries, full-text search |
| Classifications | PostgreSQL | Relational integrity, reporting |
| Validations | PostgreSQL | Historical metrics, compliance |

---

## Phase 1: PostgreSQL Schema Design

### 1.1 Entity Relationship Diagram

```
┌─────────────────────┐
│     techniques      │
│                     │
│ id (PK)             │◄──────────────────┐
│ name                │                   │
│ description         │                   │
└─────────────────────┘                   │
         ▲                                │
         │ FK                             │
┌────────┴────────────┐      ┌────────────┴───────────┐    ┌─────────────────┐
│ classification_types│      │ technique_regulations  │    │   regulations   │
│                     │      │                        │    │                 │
│ id (PK)             │      │ id (PK)                │    │ id (PK)         │
│ name                │      │ technique_id (FK)      │───►│ source          │
│ technique_id (FK)───┼──────│ regulation_id (FK)     │◄───│ article         │
│ description         │      │ justification          │    │ title           │
└─────────────────────┘      │ rationale              │    │ full_text       │
         ▲                   └────────────────────────┘    │ summary         │
         │ FK                                              └─────────────────┘
         │                                                         ▲
┌────────┴──────────────────┐         ┌─────────────────┐          │
│ classifications_on_jobs   │         │      jobs       │          │
│                           │         │                 │          │
│ id (PK)                   │    ┌───►│ id (PK, UUID)   │          │
│ job_id (FK)───────────────┼────┘    │ title           │          │
│ column_name               │         │ status          │          │
│ classification_type_id(FK)│         │ file_path       │          │
│ reasoning                 │         │ columns (JSON)  │          │
│ generalization_level      │         │ row_count       │          │
│ created_at                │         │ thresholds(JSON)│          │
└───────────┬───────────────┘         │ created_at      │          │
            │                         │ updated_at      │          │
            │ FK                      └────────┬────────┘          │
            ▼                                  │                   │
┌─────────────────────────────┐                │                   │
│ classification_regulations  │                │                   │
│                             │                │                   │
│ id (PK)                     │                │                   │
│ classification_on_job_id(FK)│                │                   │
│ regulation_id (FK)──────────┼────────────────┼───────────────────┘
│ relevance                   │                │
└─────────────────────────────┘                │
                                               │
┌─────────────────┐       ┌────────────────────┴───┐
│   validations   │       │   validation_on_jobs   │
│                 │       │                        │
│ id (PK)         │◄──────│ validation_id (FK)     │
│ name            │       │ job_id (FK)────────────┘
│ description     │       │ value (FLOAT)          │
│ default_min     │       │ threshold_used (FLOAT) │
│ default_target  │       │ passed (BOOLEAN)       │
└─────────────────┘       │ created_at             │
                          └────────────────────────┘
```

### 1.2 Table Definitions

**File: `db/init/001_schema.sql`**

```sql
-- ============================================
-- LOOKUP TABLES (Seeded once, rarely changed)
-- ============================================

-- Masking techniques
CREATE TABLE techniques (
    id VARCHAR(50) PRIMARY KEY,           -- 'SUPPRESS', 'GENERALIZE', etc.
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Classification types with linked technique
CREATE TABLE classification_types (
    id VARCHAR(50) PRIMARY KEY,           -- 'direct_identifier', 'quasi_identifier', etc.
    name VARCHAR(100) NOT NULL,
    technique_id VARCHAR(50) NOT NULL REFERENCES techniques(id),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Regulations (PDPL articles, SAMA requirements)
CREATE TABLE regulations (
    id VARCHAR(50) PRIMARY KEY,           -- 'PDPL-Art-11', 'SAMA-2.6.2'
    source VARCHAR(20) NOT NULL,          -- 'PDPL' or 'SAMA'
    article_number VARCHAR(20) NOT NULL,  -- '11', '2.6.2'
    title VARCHAR(255) NOT NULL,
    full_text TEXT NOT NULL,
    summary TEXT,                          -- Concise version for prompts
    applies_to TEXT[],                     -- Array: ['SUPPRESS', 'direct_identifiers']
    created_at TIMESTAMP DEFAULT NOW()
);

-- Which regulations justify each technique (many-to-many)
CREATE TABLE technique_regulations (
    id SERIAL PRIMARY KEY,
    technique_id VARCHAR(50) NOT NULL REFERENCES techniques(id),
    regulation_id VARCHAR(50) NOT NULL REFERENCES regulations(id),
    justification TEXT NOT NULL,          -- Why this regulation applies
    rationale TEXT,                        -- Detailed explanation
    priority INT DEFAULT 1,               -- For ordering citations
    UNIQUE(technique_id, regulation_id)
);

-- Validation metric definitions
CREATE TABLE validations (
    id VARCHAR(50) PRIMARY KEY,           -- 'k_anonymity', 'l_diversity', 't_closeness'
    name VARCHAR(100) NOT NULL,
    description TEXT,
    default_minimum FLOAT,
    default_target FLOAT,
    is_lower_better BOOLEAN DEFAULT FALSE, -- TRUE for t_closeness
    created_at TIMESTAMP DEFAULT NOW()
);

-- Saudi data patterns for auto-detection
CREATE TABLE saudi_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(50) NOT NULL,     -- 'national_id', 'iban', etc.
    regex_pattern VARCHAR(255) NOT NULL,
    classification_type_id VARCHAR(50) REFERENCES classification_types(id),
    regulation_id VARCHAR(50) REFERENCES regulations(id),
    description TEXT,
    UNIQUE(pattern_name)
);

-- ============================================
-- DATA TABLES (Created per job)
-- ============================================

-- Jobs (replaces Redis session for persistence)
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL DEFAULT 'New Job',
    status VARCHAR(50) NOT NULL DEFAULT 'idle',
    file_path VARCHAR(500),
    columns JSONB,                         -- Array of column names
    row_count INT,
    sample_data JSONB,                     -- First N rows for preview
    thresholds JSONB,                      -- {k_anonymity: {min, target}, ...}
    masked_path VARCHAR(500),              -- Output file path
    report_path VARCHAR(500),              -- PDF report path
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Per-column classifications for each job
CREATE TABLE classifications_on_jobs (
    id SERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    column_name VARCHAR(255) NOT NULL,
    classification_type_id VARCHAR(50) NOT NULL REFERENCES classification_types(id),
    reasoning TEXT,                        -- AI's natural language explanation
    generalization_level INT DEFAULT 0,   -- 0-3 for quasi-identifiers
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(job_id, column_name)
);

-- Regulation citations for each classification
CREATE TABLE classification_regulations (
    id SERIAL PRIMARY KEY,
    classification_on_job_id INT NOT NULL REFERENCES classifications_on_jobs(id) ON DELETE CASCADE,
    regulation_id VARCHAR(50) NOT NULL REFERENCES regulations(id),
    relevance TEXT,                        -- Why this regulation applies to this column
    UNIQUE(classification_on_job_id, regulation_id)
);

-- Validation results per job
CREATE TABLE validation_on_jobs (
    id SERIAL PRIMARY KEY,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    validation_id VARCHAR(50) NOT NULL REFERENCES validations(id),
    value FLOAT NOT NULL,                  -- Computed metric value
    threshold_used FLOAT,                  -- Threshold that was applied
    passed BOOLEAN NOT NULL,
    details JSONB,                         -- Additional metric details
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(job_id, validation_id)
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(created_at DESC);
CREATE INDEX idx_classifications_job ON classifications_on_jobs(job_id);
CREATE INDEX idx_classification_regs ON classification_regulations(classification_on_job_id);
CREATE INDEX idx_validation_job ON validation_on_jobs(job_id);
CREATE INDEX idx_regulations_source ON regulations(source);
CREATE INDEX idx_technique_regs_tech ON technique_regulations(technique_id);

-- Full-text search on regulations
CREATE INDEX idx_regulations_fts ON regulations
    USING GIN(to_tsvector('english', full_text || ' ' || title));
```

### 1.3 Seed Data

**File: `db/init/002_seed_data.sql`**

```sql
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
('direct_identifier', 'Direct Identifier', 'SUPPRESS', 'Data that directly identifies an individual (name, ID, phone)'),
('quasi_identifier', 'Quasi Identifier', 'GENERALIZE', 'Data that could identify when combined (age, city, gender)'),
('linkage_identifier', 'Linkage Identifier', 'PSEUDONYMIZE', 'IDs used for record linking (customer_id, account_id)'),
('date_column', 'Date Column', 'DATE_SHIFT', 'Date/timestamp fields'),
('sensitive_attribute', 'Sensitive Attribute', 'KEEP', 'Analysis target data (amount, fraud_flag)');

-- ============================================
-- REGULATIONS (PDPL)
-- ============================================
INSERT INTO regulations (id, source, article_number, title, full_text, summary, applies_to) VALUES
('PDPL-Art-5', 'PDPL', '5', 'Sensitive Personal Data',
 'Sensitive personal data includes data revealing racial or ethnic origin, religious beliefs, health data, genetic data, financial data, and criminal records.',
 'Defines sensitive data categories requiring extra protection',
 ARRAY['sensitive_attribute', 'KEEP']),

('PDPL-Art-10', 'PDPL', '10', 'Consent Requirements',
 'Processing personal data requires consent from the data subject, which must be explicit, informed, and freely given.',
 'Explicit consent required for processing',
 ARRAY['direct_identifier', 'SUPPRESS']),

('PDPL-Art-11', 'PDPL', '11', 'Data Minimization',
 'Personal data must be limited to the minimum necessary for the purposes for which it is processed.',
 'Collect only minimum necessary data',
 ARRAY['SUPPRESS', 'direct_identifier', 'data_retention']),

('PDPL-Art-15', 'PDPL', '15', 'Disclosure Restrictions',
 'Personal data may only be disclosed with consent or in anonymized form that prevents identification.',
 'Disclosure requires consent OR anonymization',
 ARRAY['SUPPRESS', 'GENERALIZE', 'disclosure']),

('PDPL-Art-17', 'PDPL', '17', 'Data Quality',
 'Personal data must be accurate, complete, and kept up to date where necessary.',
 'Maintain data accuracy and quality',
 ARRAY['quasi_identifier', 'GENERALIZE']),

('PDPL-Art-18', 'PDPL', '18', 'Storage Limitation',
 'Personal data must not be stored longer than necessary for the specified purpose.',
 'Delete data when no longer needed',
 ARRAY['SUPPRESS', 'retention']),

('PDPL-Art-19', 'PDPL', '19', 'Technical Measures',
 'Controllers must implement appropriate technical measures to protect personal data.',
 'Implement technical safeguards',
 ARRAY['PSEUDONYMIZE', 'linkage_identifier', 'technical']),

('PDPL-Art-23', 'PDPL', '23', 'Security Breach',
 'In case of breach, controller must notify authority within 72 hours if risk to rights.',
 'Breach notification required',
 ARRAY['security', 'breach']),

('PDPL-Art-24', 'PDPL', '24', 'Credit Data',
 'Processing credit data requires explicit consent and is subject to additional safeguards.',
 'Extra protection for credit data',
 ARRAY['sensitive_attribute', 'financial']),

('PDPL-Art-29', 'PDPL', '29', 'Cross-Border Transfers',
 'Transfer outside Saudi Arabia requires adequate protection level in destination country.',
 'Cross-border transfers need adequate protection',
 ARRAY['transfer', 'international']),

('PDPL-Art-31', 'PDPL', '31', 'Penalties',
 'Violations subject to fines up to 5 million SAR and/or imprisonment.',
 'Significant penalties for non-compliance',
 ARRAY['compliance', 'penalties']);

-- ============================================
-- REGULATIONS (SAMA)
-- ============================================
INSERT INTO regulations (id, source, article_number, title, full_text, summary, applies_to) VALUES
('SAMA-2.6.1', 'SAMA', '2.6.1', 'Data Classification',
 'Financial institutions must classify data based on sensitivity and implement appropriate controls.',
 'Classify and protect based on sensitivity',
 ARRAY['classification', 'direct_identifier', 'quasi_identifier']),

('SAMA-2.6.2', 'SAMA', '2.6.2', 'Data Security',
 'Personal data must be secured in Saudi facilities with PCI DSS compliance for payment data.',
 'Saudi-based storage, PCI compliance',
 ARRAY['security', 'storage', 'SUPPRESS']),

('SAMA-2.6.3', 'SAMA', '2.6.3', 'Third-Party Sharing',
 'Sharing with third parties requires consent OR data must be anonymized.',
 'Third-party sharing needs consent or anonymization',
 ARRAY['sharing', 'SUPPRESS', 'GENERALIZE']),

('SAMA-OB', 'SAMA', 'Open Banking', 'Open Banking Framework',
 'TPPs may access customer data with consent. Data sharing must be secure and auditable.',
 'Secure data sharing for open banking',
 ARRAY['api', 'sharing', 'PSEUDONYMIZE']),

('SAMA-BCT', 'SAMA', 'BCT/15631', 'Cybersecurity Framework',
 'Financial institutions must implement comprehensive cybersecurity controls.',
 'Cybersecurity controls mandatory',
 ARRAY['security', 'technical']);

-- ============================================
-- TECHNIQUE-REGULATION MAPPINGS
-- ============================================
INSERT INTO technique_regulations (technique_id, regulation_id, justification, rationale, priority) VALUES
-- SUPPRESS justifications
('SUPPRESS', 'PDPL-Art-11', 'Direct identifiers must be suppressed per data minimization principle',
 'Names, IDs, and contact info exceed minimum necessary for most analytics', 1),
('SUPPRESS', 'PDPL-Art-15', 'Suppression ensures disclosure does not enable identification',
 'Complete removal is the safest anonymization for direct identifiers', 2),
('SUPPRESS', 'SAMA-2.6.2', 'Sensitive identifiers must be removed before any processing outside secure facility',
 'SAMA requires personal data secured in Saudi facilities', 3),

-- GENERALIZE justifications
('GENERALIZE', 'PDPL-Art-11', 'Generalization reduces data to minimum necessary granularity',
 'Age ranges and location hierarchies preserve utility while reducing precision', 1),
('GENERALIZE', 'PDPL-Art-17', 'Generalized data maintains accuracy at aggregate level',
 'Ranges remain accurate representations while reducing identification risk', 2),
('GENERALIZE', 'SAMA-2.6.3', 'Generalization enables compliant third-party sharing',
 'Generalized quasi-identifiers can be shared with reduced risk', 3),

-- PSEUDONYMIZE justifications
('PSEUDONYMIZE', 'PDPL-Art-19', 'Pseudonymization is a recognized technical protection measure',
 'HMAC-based pseudonyms enable linking without exposing original IDs', 1),
('PSEUDONYMIZE', 'SAMA-OB', 'Pseudonymous identifiers support secure open banking data flows',
 'TPPs can work with pseudonymous IDs for cross-dataset analysis', 2),

-- DATE_SHIFT justifications
('DATE_SHIFT', 'PDPL-Art-11', 'Date shifting minimizes temporal precision while preserving patterns',
 'Random offsets preserve relative timing for fraud detection', 1),

-- KEEP justifications
('KEEP', 'PDPL-Art-5', 'Sensitive attributes must be preserved for legitimate analysis purposes',
 'Fraud flags and amounts are needed for model training', 1),
('KEEP', 'PDPL-Art-24', 'Financial data retained for credit scoring and fraud detection',
 'Transaction patterns require sensitive attribute preservation', 2);

-- ============================================
-- VALIDATIONS (Metric definitions)
-- ============================================
INSERT INTO validations (id, name, description, default_minimum, default_target, is_lower_better) VALUES
('k_anonymity', 'K-Anonymity', 'Each record indistinguishable from k-1 others on quasi-identifiers', 5, 10, FALSE),
('l_diversity', 'L-Diversity', 'At least l distinct sensitive values in each equivalence class', 2, 3, FALSE),
('t_closeness', 'T-Closeness', 'Distribution of sensitive values in each class close to overall distribution', 0.2, 0.15, TRUE),
('risk_score', 'Risk Score', 'Composite re-identification risk percentage', 20, 10, TRUE);

-- ============================================
-- SAUDI PATTERNS
-- ============================================
INSERT INTO saudi_patterns (pattern_name, regex_pattern, classification_type_id, regulation_id, description) VALUES
('national_id', '^1\d{9}$', 'direct_identifier', 'PDPL-Art-11', 'Saudi National ID (starts with 1)'),
('iqama', '^2\d{9}$', 'direct_identifier', 'PDPL-Art-11', 'Resident ID/Iqama (starts with 2)'),
('phone', '^(\+966|05)\d{8}$', 'direct_identifier', 'PDPL-Art-11', 'Saudi phone number'),
('iban', '^SA\d{22}$', 'direct_identifier', 'SAMA-2.6.2', 'Saudi IBAN'),
('card_pan', '^\d{16}$', 'direct_identifier', 'SAMA-2.6.2', 'Payment card number (16 digits)');
```

---

## Phase 2: Docker Compose Setup

### 2.1 Add PostgreSQL Service

**File: `docker-compose.yml`** (MODIFY)

```yaml
services:
  # ... existing services ...

  postgres:
    image: postgres:15-alpine
    container_name: sadnxai-postgres
    environment:
      POSTGRES_DB: sadnxai
      POSTGRES_USER: sadnxai
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-sadnxai_secure_pass}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sadnxai -d sadnxai"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - sadnxai-network

  redis:
    # ... keep existing redis config ...

  chat-service:
    # ... existing config ...
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    environment:
      # ... existing env vars ...
      DATABASE_URL: postgresql://sadnxai:${POSTGRES_PASSWORD:-sadnxai_secure_pass}@postgres:5432/sadnxai

volumes:
  postgres_data:
  # ... other volumes ...
```

---

## Phase 3: Database Access Layer

### 3.1 Database Client

**File: `shared/database.py`** (NEW)

```python
"""PostgreSQL client for SADNxAI"""
import asyncpg
import os
from typing import Optional, List, Dict, Any
from uuid import UUID

class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=os.getenv("DATABASE_URL", "postgresql://sadnxai:sadnxai_secure_pass@postgres:5432/sadnxai"),
                min_size=2,
                max_size=10
            )
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    # ============================================
    # REGULATION QUERIES (for LLM tool)
    # ============================================

    @classmethod
    async def query_regulations_by_technique(cls, technique: str) -> List[Dict[str, Any]]:
        """Get regulations for a masking technique"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT r.id, r.source, r.article_number, r.title, r.summary,
                   tr.justification, tr.rationale
            FROM technique_regulations tr
            JOIN regulations r ON tr.regulation_id = r.id
            WHERE tr.technique_id = $1
            ORDER BY tr.priority
        """, technique.upper())
        return [dict(r) for r in rows]

    @classmethod
    async def query_regulations_by_classification_type(cls, classification_type: str) -> List[Dict[str, Any]]:
        """Get regulations for a classification type (via its technique)"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT r.id, r.source, r.article_number, r.title, r.summary,
                   tr.justification, tr.rationale, ct.name as classification_name
            FROM classification_types ct
            JOIN techniques t ON ct.technique_id = t.id
            JOIN technique_regulations tr ON tr.technique_id = t.id
            JOIN regulations r ON tr.regulation_id = r.id
            WHERE ct.id = $1
            ORDER BY tr.priority
        """, classification_type)
        return [dict(r) for r in rows]

    @classmethod
    async def query_regulations_by_ids(cls, regulation_ids: List[str]) -> List[Dict[str, Any]]:
        """Get full regulation details by IDs"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT id, source, article_number, title, full_text, summary
            FROM regulations
            WHERE id = ANY($1)
        """, regulation_ids)
        return [dict(r) for r in rows]

    @classmethod
    async def search_regulations(cls, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Full-text search on regulation content"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT id, source, article_number, title, summary,
                   ts_rank(to_tsvector('english', full_text || ' ' || title),
                           plainto_tsquery('english', $1)) as rank
            FROM regulations
            WHERE to_tsvector('english', full_text || ' ' || title) @@ plainto_tsquery('english', $1)
            ORDER BY rank DESC
            LIMIT $2
        """, query, limit)
        return [dict(r) for r in rows]

    @classmethod
    async def detect_saudi_pattern(cls, column_name: str) -> Optional[Dict[str, Any]]:
        """Detect Saudi pattern by column name hint"""
        pool = await cls.get_pool()
        row = await pool.fetchrow("""
            SELECT sp.*, ct.name as classification_name, t.id as technique_id,
                   r.title as regulation_title, r.summary as regulation_summary
            FROM saudi_patterns sp
            JOIN classification_types ct ON sp.classification_type_id = ct.id
            JOIN techniques t ON ct.technique_id = t.id
            LEFT JOIN regulations r ON sp.regulation_id = r.id
            WHERE $1 ILIKE '%' || sp.pattern_name || '%'
            LIMIT 1
        """, column_name)
        return dict(row) if row else None

    @classmethod
    async def get_classification_types(cls) -> List[Dict[str, Any]]:
        """Get all classification types with their techniques"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT ct.id, ct.name, ct.description, t.id as technique_id, t.name as technique_name
            FROM classification_types ct
            JOIN techniques t ON ct.technique_id = t.id
            ORDER BY ct.id
        """)
        return [dict(r) for r in rows]

    # ============================================
    # JOB CRUD
    # ============================================

    @classmethod
    async def create_job(cls, job_id: UUID, title: str = "New Job") -> Dict[str, Any]:
        """Create a new job"""
        pool = await cls.get_pool()
        row = await pool.fetchrow("""
            INSERT INTO jobs (id, title, status)
            VALUES ($1, $2, 'idle')
            RETURNING *
        """, job_id, title)
        return dict(row)

    @classmethod
    async def get_job(cls, job_id: UUID) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        pool = await cls.get_pool()
        row = await pool.fetchrow("SELECT * FROM jobs WHERE id = $1", job_id)
        return dict(row) if row else None

    @classmethod
    async def update_job(cls, job_id: UUID, **kwargs) -> Optional[Dict[str, Any]]:
        """Update job fields"""
        pool = await cls.get_pool()

        # Build SET clause dynamically
        set_parts = []
        values = [job_id]
        for i, (key, value) in enumerate(kwargs.items(), start=2):
            set_parts.append(f"{key} = ${i}")
            values.append(value)

        set_parts.append("updated_at = NOW()")
        set_clause = ", ".join(set_parts)

        row = await pool.fetchrow(f"""
            UPDATE jobs SET {set_clause}
            WHERE id = $1
            RETURNING *
        """, *values)
        return dict(row) if row else None

    @classmethod
    async def list_jobs(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent jobs"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT * FROM jobs
            ORDER BY updated_at DESC
            LIMIT $1
        """, limit)
        return [dict(r) for r in rows]

    @classmethod
    async def delete_job(cls, job_id: UUID) -> bool:
        """Delete a job"""
        pool = await cls.get_pool()
        result = await pool.execute("DELETE FROM jobs WHERE id = $1", job_id)
        return result == "DELETE 1"

    # ============================================
    # CLASSIFICATION CRUD
    # ============================================

    @classmethod
    async def save_classifications(cls, job_id: UUID, classifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Save classifications for a job (replace existing)"""
        pool = await cls.get_pool()

        # Delete existing classifications
        await pool.execute("DELETE FROM classifications_on_jobs WHERE job_id = $1", job_id)

        results = []
        for c in classifications:
            row = await pool.fetchrow("""
                INSERT INTO classifications_on_jobs
                (job_id, column_name, classification_type_id, reasoning, generalization_level)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
            """, job_id, c['column_name'], c['classification_type_id'],
                c.get('reasoning'), c.get('generalization_level', 0))

            classification_id = row['id']

            # Save regulation references
            for reg in c.get('regulation_refs', []):
                await pool.execute("""
                    INSERT INTO classification_regulations
                    (classification_on_job_id, regulation_id, relevance)
                    VALUES ($1, $2, $3)
                    ON CONFLICT DO NOTHING
                """, classification_id, reg['regulation_id'], reg.get('relevance'))

            results.append(dict(row))

        return results

    @classmethod
    async def get_classifications(cls, job_id: UUID) -> List[Dict[str, Any]]:
        """Get classifications for a job with regulation references"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT coj.*, ct.name as classification_name, t.id as technique_id, t.name as technique_name,
                   COALESCE(
                       json_agg(
                           json_build_object(
                               'regulation_id', cr.regulation_id,
                               'relevance', cr.relevance,
                               'title', r.title,
                               'source', r.source
                           )
                       ) FILTER (WHERE cr.id IS NOT NULL),
                       '[]'
                   ) as regulation_refs
            FROM classifications_on_jobs coj
            JOIN classification_types ct ON coj.classification_type_id = ct.id
            JOIN techniques t ON ct.technique_id = t.id
            LEFT JOIN classification_regulations cr ON coj.id = cr.classification_on_job_id
            LEFT JOIN regulations r ON cr.regulation_id = r.id
            WHERE coj.job_id = $1
            GROUP BY coj.id, ct.name, t.id, t.name
            ORDER BY coj.column_name
        """, job_id)
        return [dict(r) for r in rows]

    # ============================================
    # VALIDATION CRUD
    # ============================================

    @classmethod
    async def save_validation_results(cls, job_id: UUID, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Save validation results for a job"""
        pool = await cls.get_pool()

        saved = []
        for r in results:
            row = await pool.fetchrow("""
                INSERT INTO validation_on_jobs
                (job_id, validation_id, value, threshold_used, passed, details)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (job_id, validation_id) DO UPDATE SET
                    value = EXCLUDED.value,
                    threshold_used = EXCLUDED.threshold_used,
                    passed = EXCLUDED.passed,
                    details = EXCLUDED.details,
                    created_at = NOW()
                RETURNING *
            """, job_id, r['validation_id'], r['value'],
                r.get('threshold_used'), r['passed'],
                r.get('details'))
            saved.append(dict(row))

        return saved

    @classmethod
    async def get_validation_results(cls, job_id: UUID) -> List[Dict[str, Any]]:
        """Get validation results for a job"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT voj.*, v.name, v.description
            FROM validation_on_jobs voj
            JOIN validations v ON voj.validation_id = v.id
            WHERE voj.job_id = $1
            ORDER BY v.id
        """, job_id)
        return [dict(r) for r in rows]
```

---

## Phase 4: query_regulations Tool

### 4.1 Tool Schema

**File: `shared/openai_schema.py`** (ADD to TOOLS)

```python
{
    "name": "query_regulations",
    "description": "Query the regulation database to find relevant PDPL/SAMA articles. Use BEFORE classifying to get accurate regulatory citations.",
    "parameters": {
        "type": "object",
        "properties": {
            "query_type": {
                "type": "string",
                "enum": ["technique", "classification_type", "search", "by_ids", "pattern"],
                "description": "Query type: 'technique' (SUPPRESS/GENERALIZE/etc), 'classification_type' (direct_identifier/quasi_identifier/etc), 'search' (free text), 'by_ids' (specific IDs), 'pattern' (detect Saudi pattern)"
            },
            "value": {
                "type": "string",
                "description": "Query value based on query_type"
            }
        },
        "required": ["query_type", "value"]
    }
}
```

### 4.2 Tool Handler

**File: `chat-service/llm/tools.py`** (ADD)

```python
async def _handle_query_regulations(self, args: Dict[str, Any]) -> Dict[str, Any]:
    """Query regulation database"""
    from shared.database import Database

    query_type = args.get("query_type", "")
    value = args.get("value", "")

    try:
        if query_type == "technique":
            results = await Database.query_regulations_by_technique(value)
        elif query_type == "classification_type":
            results = await Database.query_regulations_by_classification_type(value)
        elif query_type == "search":
            results = await Database.search_regulations(value)
        elif query_type == "by_ids":
            ids = [id.strip() for id in value.split(",")]
            results = await Database.query_regulations_by_ids(ids)
        elif query_type == "pattern":
            result = await Database.detect_saudi_pattern(value)
            results = [result] if result else []
        else:
            return {"success": False, "error": f"Unknown query_type: {query_type}"}

        return {
            "success": True,
            "query_type": query_type,
            "value": value,
            "regulations": results,
            "count": len(results)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## Phase 5: Updated classify_columns Tool

### 5.1 New Tool Schema

The classify_columns tool should now save to PostgreSQL and include regulation references.

**File: `shared/openai_schema.py`** (MODIFY classify_columns)

```python
{
    "name": "classify_columns",
    "description": "Record column classifications with regulatory citations. Call query_regulations first to get accurate citations.",
    "parameters": {
        "type": "object",
        "properties": {
            "classifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "column_name": {"type": "string"},
                        "classification_type": {
                            "type": "string",
                            "enum": ["direct_identifier", "quasi_identifier", "linkage_identifier", "date_column", "sensitive_attribute"]
                        },
                        "reasoning": {"type": "string", "description": "Natural language explanation"},
                        "generalization_level": {"type": "integer", "minimum": 0, "maximum": 3},
                        "regulation_refs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "regulation_id": {"type": "string"},
                                    "relevance": {"type": "string"}
                                },
                                "required": ["regulation_id", "relevance"]
                            }
                        }
                    },
                    "required": ["column_name", "classification_type", "reasoning", "regulation_refs"]
                },
                "description": "Classification for each column with regulatory justifications"
            }
        },
        "required": ["classifications"]
    }
}
```

### 5.2 Tool Handler

**File: `chat-service/llm/tools.py`** (MODIFY)

```python
async def _handle_classify_columns(self, args: Dict[str, Any]) -> Dict[str, Any]:
    """Save classifications to PostgreSQL"""
    from shared.database import Database

    classifications_data = args.get("classifications", [])

    if not classifications_data:
        return {"success": False, "error": "No classifications provided"}

    # Transform to DB format
    db_classifications = []
    for c in classifications_data:
        db_classifications.append({
            "column_name": c["column_name"],
            "classification_type_id": c["classification_type"],
            "reasoning": c.get("reasoning", ""),
            "generalization_level": c.get("generalization_level", 0),
            "regulation_refs": c.get("regulation_refs", [])
        })

    # Save to PostgreSQL
    job_id = self.session.id  # UUID
    saved = await Database.save_classifications(job_id, db_classifications)

    # Also update session object for backward compatibility
    # ... existing session update logic ...

    return {
        "success": True,
        "message": f"Classified {len(saved)} columns",
        "classifications": saved
    }
```

---

## Phase 6: State-Based Prompts

(Same as before - see previous plan section for prompt templates)

### Key Changes

1. Prompts reference the new tool schemas
2. ANALYZING prompt instructs LLM to call query_regulations first
3. Example shows proper regulation citation flow

---

## Phase 7: PDF Report Integration

### 7.1 Update Report Generator

**File: `validation-service/report/generator.py`** (MODIFY)

```python
async def generate_report(self, job_id: UUID) -> str:
    """Generate PDF report from PostgreSQL data"""
    from shared.database import Database

    # Get job data
    job = await Database.get_job(job_id)
    classifications = await Database.get_classifications(job_id)
    validations = await Database.get_validation_results(job_id)

    # Build PDF with:
    # 1. Job summary
    # 2. Classification table (column, type, technique, regulations, reasoning)
    # 3. Validation metrics table
    # 4. Detailed regulatory justifications section

    for c in classifications:
        # Each classification has regulation_refs with full details
        reg_citations = ", ".join([
            f"{r['source']} {r['regulation_id'].split('-')[-1]}"
            for r in c['regulation_refs']
        ])

        self._add_table_row([
            c['column_name'],
            c['classification_name'],
            c['technique_name'],
            reg_citations,
            c['reasoning'][:80] + "..."
        ])

    # Detailed justifications section
    self._add_heading("Regulatory Justifications")
    for c in classifications:
        self._add_paragraph(f"**{c['column_name']}** ({c['technique_name']})")
        self._add_paragraph(c['reasoning'], indent=True)
        for r in c['regulation_refs']:
            self._add_paragraph(f"• {r['regulation_id']}: {r['title']} - {r['relevance']}", indent=True)
```

---

## Implementation Order

### Step 1: Database Setup
1. Create `db/init/` directory
2. Write `001_schema.sql` and `002_seed_data.sql`
3. Update `docker-compose.yml` with postgres service
4. Test: `docker compose up postgres` and verify tables

### Step 2: Database Access Layer
1. Create `shared/database.py`
2. Add `asyncpg` to requirements
3. Test: Write unit tests for CRUD operations

### Step 3: query_regulations Tool
1. Add tool schema to `openai_schema.py`
2. Implement handler in `tools.py`
3. Add to VALID_TOOLS in `ollama_adapter.py`
4. Test: Manual tool call verification

### Step 4: Update classify_columns Tool
1. Modify tool schema for new format
2. Update handler to save to PostgreSQL
3. Test: Classification flow with regulation refs

### Step 5: State-Based Prompts
1. Create `shared/prompts/` directory
2. Write prompt templates
3. Update `ollama_adapter.py`
4. Test: Verify prompt switching by state

### Step 6: PDF Report Integration
1. Update report generator to query PostgreSQL
2. Add regulatory justifications section
3. Test: Generate PDF and verify content

### Step 7: Integration Testing
1. End-to-end flow test
2. Verify LLM cites regulations correctly
3. Check PDF report quality

---

## Summary

| Component | Before | After |
|-----------|--------|-------|
| Job Storage | Redis only | PostgreSQL (source of truth) + Redis (cache) |
| Regulations | Hardcoded in prompt | PostgreSQL with full-text search |
| Classifications | JSON in session | Normalized tables with FK to types/techniques |
| Validations | JSON in session | Normalized table with history |
| Prompts | Monolithic (~2,800 tokens) | State-based (400-1,200 tokens) |
| LLM Regulation Access | None (static prompt) | query_regulations tool |
| PDF Report | Hardcoded mappings | Query from DB with justifications |

---

## Implementation Progress

### Completed

- [x] **Phase 1: Database Setup**
  - [x] Created `db/init/001_schema.sql` with normalized schema
  - [x] Created `db/init/002_seed_data.sql` with lookup data
  - [x] Updated `docker-compose.yml` with PostgreSQL service
  - [x] Created `shared/database.py` access layer
  - [x] Added `asyncpg` to requirements.txt files

- [x] **Phase 4: query_regulations Tool**
  - [x] Added tool schema to `shared/openai_schema.py`
  - [x] Implemented handler in `chat-service/llm/tools.py`
  - [x] Added to VALID_TOOLS in `ollama_adapter.py`

- [x] **Phase 6: State-Based Prompts**
  - [x] Created `shared/prompts/` directory
  - [x] Implemented state-based templates (idle, analyzing, proposed, approved, completed, failed)
  - [x] Updated `ollama_adapter.py` to use state-based prompts

### In Progress

- [ ] **Phase 5: Updated classify_columns Tool**
  - [ ] Update tool schema for new format with regulation_refs
  - [ ] Update handler to save to PostgreSQL

### Pending

- [ ] **Phase 7: PDF Report Integration**
  - [ ] Update report generator to query PostgreSQL
  - [ ] Add regulatory justifications section

- [ ] **Testing**
  - [ ] Test database setup and queries
  - [ ] End-to-end integration testing
