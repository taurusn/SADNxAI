"""
PostgreSQL Database Access Layer for SADNxAI

Provides async database operations for:
- Regulation queries (for LLM tool)
- Job CRUD operations
- Classification storage
- Validation results
"""
import asyncpg
import os
import json
from typing import Optional, List, Dict, Any
from uuid import UUID


class Database:
    """Async PostgreSQL client with connection pooling"""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        """Get or create connection pool"""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                dsn=os.getenv(
                    "DATABASE_URL",
                    "postgresql://sadnxai:sadnxai_secure_pass@localhost:5432/sadnxai"
                ),
                min_size=2,
                max_size=10
            )
        return cls._pool

    @classmethod
    async def close(cls):
        """Close connection pool"""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    # ============================================
    # REGULATION QUERIES (for LLM tool)
    # ============================================

    @classmethod
    async def query_regulations_by_technique(cls, technique: str) -> List[Dict[str, Any]]:
        """Get regulations that justify a masking technique"""
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
        """Get regulations for a classification type (via its linked technique)"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT r.id, r.source, r.article_number, r.title, r.summary,
                   tr.justification, tr.rationale,
                   ct.name as classification_name, t.id as technique_id, t.name as technique_name
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
            SELECT id, source, article_number, title, full_text, summary, applies_to
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
            SELECT sp.pattern_name, sp.regex_pattern, sp.description,
                   ct.id as classification_type_id, ct.name as classification_name,
                   t.id as technique_id, t.name as technique_name,
                   r.id as regulation_id, r.title as regulation_title, r.summary as regulation_summary
            FROM saudi_patterns sp
            JOIN classification_types ct ON sp.classification_type_id = ct.id
            JOIN techniques t ON ct.technique_id = t.id
            LEFT JOIN regulations r ON sp.regulation_id = r.id
            WHERE $1 ILIKE '%' || sp.pattern_name || '%'
            LIMIT 1
        """, column_name)
        return dict(row) if row else None

    @classmethod
    async def get_all_regulations(cls) -> List[Dict[str, Any]]:
        """Get all regulations"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT id, source, article_number, title, summary, applies_to
            FROM regulations
            ORDER BY source, article_number
        """)
        return [dict(r) for r in rows]

    @classmethod
    async def get_classification_types(cls) -> List[Dict[str, Any]]:
        """Get all classification types with their linked techniques"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT ct.id, ct.name, ct.description,
                   t.id as technique_id, t.name as technique_name, t.description as technique_description
            FROM classification_types ct
            JOIN techniques t ON ct.technique_id = t.id
            ORDER BY ct.id
        """)
        return [dict(r) for r in rows]

    @classmethod
    async def get_validation_definitions(cls) -> List[Dict[str, Any]]:
        """Get all validation metric definitions"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT id, name, description, default_minimum, default_target, is_lower_better
            FROM validations
            ORDER BY id
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
        """Update job fields dynamically"""
        pool = await cls.get_pool()

        if not kwargs:
            return await cls.get_job(job_id)

        # Build SET clause dynamically
        set_parts = []
        values = [job_id]
        for i, (key, value) in enumerate(kwargs.items(), start=2):
            set_parts.append(f"{key} = ${i}")
            # Convert dict/list to JSON string for JSONB columns
            if isinstance(value, (dict, list)):
                values.append(json.dumps(value))
            else:
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
    async def list_jobs(cls, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """List recent jobs with pagination"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT id, title, status, file_path, row_count, created_at, updated_at
            FROM jobs
            ORDER BY updated_at DESC
            LIMIT $1 OFFSET $2
        """, limit, offset)
        return [dict(r) for r in rows]

    @classmethod
    async def delete_job(cls, job_id: UUID) -> bool:
        """Delete a job and all related data (cascades)"""
        pool = await cls.get_pool()
        result = await pool.execute("DELETE FROM jobs WHERE id = $1", job_id)
        return result == "DELETE 1"

    # ============================================
    # CLASSIFICATION CRUD
    # ============================================

    @classmethod
    async def save_classifications(
        cls,
        job_id: UUID,
        classifications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Save classifications for a job (replaces existing).

        Each classification dict should have:
        - column_name: str
        - classification_type_id: str (direct_identifier, quasi_identifier, etc.)
        - reasoning: str (optional)
        - generalization_level: int (optional, default 0)
        - regulation_refs: list of {regulation_id, relevance} (optional)
        """
        pool = await cls.get_pool()

        # Use a single connection with transaction for all operations
        async with pool.acquire() as conn:
            async with conn.transaction():
                # Delete existing classifications for this job
                await conn.execute(
                    "DELETE FROM classifications_on_jobs WHERE job_id = $1",
                    job_id
                )

                results = []
                for c in classifications:
                    # Insert classification
                    row = await conn.fetchrow("""
                        INSERT INTO classifications_on_jobs
                        (job_id, column_name, classification_type_id, reasoning, generalization_level)
                        VALUES ($1, $2, $3, $4, $5)
                        RETURNING *
                    """, job_id, c['column_name'], c['classification_type_id'],
                        c.get('reasoning'), c.get('generalization_level', 0))

                    classification_id = row['id']

                    # Save regulation references (skip invalid regulation IDs)
                    for reg in c.get('regulation_refs', []):
                        reg_id = reg.get('regulation_id', '')
                        # Check if regulation exists before inserting
                        exists = await conn.fetchval(
                            "SELECT 1 FROM regulations WHERE id = $1", reg_id
                        )
                        if exists:
                            await conn.execute("""
                                INSERT INTO classification_regulations
                                (classification_on_job_id, regulation_id, relevance)
                                VALUES ($1, $2, $3)
                                ON CONFLICT (classification_on_job_id, regulation_id) DO UPDATE
                                SET relevance = EXCLUDED.relevance
                            """, classification_id, reg_id, reg.get('relevance'))

                    results.append(dict(row))

        return results

    @classmethod
    async def get_classifications(cls, job_id: UUID) -> List[Dict[str, Any]]:
        """Get classifications for a job with regulation references and technique info"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT
                coj.id,
                coj.job_id,
                coj.column_name,
                coj.classification_type_id,
                coj.reasoning,
                coj.generalization_level,
                coj.created_at,
                ct.name as classification_name,
                t.id as technique_id,
                t.name as technique_name,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'regulation_id', cr.regulation_id,
                            'relevance', cr.relevance,
                            'title', r.title,
                            'source', r.source,
                            'article_number', r.article_number
                        )
                    ) FILTER (WHERE cr.id IS NOT NULL),
                    '[]'::json
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
    async def save_validation_results(
        cls,
        job_id: UUID,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Save validation results for a job.

        Each result dict should have:
        - validation_id: str (k_anonymity, l_diversity, etc.)
        - value: float
        - threshold_used: float (optional)
        - passed: bool
        - details: dict (optional)
        """
        pool = await cls.get_pool()

        saved = []
        for r in results:
            details_json = json.dumps(r.get('details')) if r.get('details') else None

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
                r.get('threshold_used'), r['passed'], details_json)
            saved.append(dict(row))

        return saved

    @classmethod
    async def get_validation_results(cls, job_id: UUID) -> List[Dict[str, Any]]:
        """Get validation results for a job with metric definitions"""
        pool = await cls.get_pool()
        rows = await pool.fetch("""
            SELECT
                voj.id,
                voj.job_id,
                voj.validation_id,
                voj.value,
                voj.threshold_used,
                voj.passed,
                voj.details,
                voj.created_at,
                v.name,
                v.description,
                v.is_lower_better
            FROM validation_on_jobs voj
            JOIN validations v ON voj.validation_id = v.id
            WHERE voj.job_id = $1
            ORDER BY v.id
        """, job_id)
        return [dict(r) for r in rows]

    # ============================================
    # UTILITY METHODS
    # ============================================

    @classmethod
    async def get_job_summary(cls, job_id: UUID) -> Optional[Dict[str, Any]]:
        """Get complete job summary including classifications and validations"""
        job = await cls.get_job(job_id)
        if not job:
            return None

        classifications = await cls.get_classifications(job_id)
        validations = await cls.get_validation_results(job_id)

        return {
            **job,
            'classifications': classifications,
            'validation_results': validations
        }
