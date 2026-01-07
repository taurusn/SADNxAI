# SADNxAI: SDS vs Implementation Gap Analysis Report

## Executive Summary

| Dimension | Compliance | Critical Gaps |
|-----------|------------|---------------|
| **Architecture** | 40% | 3 missing services, no message queues |
| **Security** | 25% | No auth, CORS wildcard, no encryption |
| **Data Design** | 53% | 8/17 tables missing |
| **Masking Service** | 60% | Wrong execution order, missing levels |
| **Validation Service** | 85% | Metrics correct, wrong architecture |
| **Chat/Orchestrator** | 50% | Different model (LLM-based) |
| **Regulatory Compliance** | 35% | No audit trail, no Vault |

---

## 1. Architecture Gaps

### Services Comparison

| SDS Service | Port | Status | Actual Implementation |
|-------------|------|--------|----------------------|
| Orchestrator | 8000 | PARTIAL | chat-service (LLM-based) |
| NLP Service | 8001 | MISSING | LLM replaces spaCy |
| Masking Service | 8002 | EXISTS | masking-service |
| Validation Service | 8003 | EXISTS | validation-service |
| Storage Service | 8004 | MISSING | Filesystem only |
| Audit Service | 8005 | MISSING | No audit trail |
| Federation Gateway | 8443 | MISSING | No federation |

### Infrastructure Gaps

| Component | SDS | Actual | Gap |
|-----------|-----|--------|-----|
| Message Queue | RabbitMQ (5 queues) | None | CRITICAL |
| Object Storage | MinIO (5 phases) | Docker volume | CRITICAL |
| Secret Management | HashiCorp Vault | Env vars | CRITICAL |
| Monitoring | Prometheus/Grafana | None | HIGH |

---

## 2. Security Gaps

### Critical Security Issues

| Issue | File | Status |
|-------|------|--------|
| CORS wildcard `*` | masking-service/main.py:27 | CRITICAL |
| CORS wildcard `*` | validation-service/main.py:27 | CRITICAL |
| No authentication | All API routes | CRITICAL |
| No encryption at rest | All storage | CRITICAL |
| DB ports exposed | docker-compose.yml:77,90 | CRITICAL |
| No Redis password | docker-compose.yml | CRITICAL |
| Path traversal risk | chat-service/api/routes.py:493 | HIGH |
| No TLS enforcement | All services | HIGH |

### Compliance Status

| Regulation | Score | Critical Gap |
|------------|-------|--------------|
| PDPL | 40% | No audit logs (Art. 31) |
| SAMA | 30% | No encryption (2.6.2) |
| NCA ECC-2 | 25% | No access control |
| MOH IS0303 | 20% | No 7-year retention |

---

## 3. Masking Service Gaps

### Transformation Algorithms

| Technique | SDS | Implementation | Gap |
|-----------|-----|----------------|-----|
| Suppression | Yes | Yes | Low |
| Generalization | 6 levels | 4 levels | 2 levels missing |
| Pseudonymization | 24 chars + Vault | 12 chars, no Vault | Security gap |
| Date Shifting | Patient-level | Row-level | Interval broken |
| NLP Redaction | 11 entity types | 6 types (regex) | No NLP Service |

### Critical Bugs Found

1. **Wrong execution order**: Text scrub runs FIRST (should be LAST)
2. **Gender level bug**: `generalizer.py:363` uses `location_level` instead of `age_level`
3. **Missing IBAN pattern**: Saudi IBAN `SA\d{22}` not detected

---

## 4. Validation Service Gaps

### Privacy Metrics (Well Implemented)

| Metric | SDS | Implementation | Status |
|--------|-----|----------------|--------|
| k-anonymity | Min group size | Correct | PASS |
| l-diversity | Distinct values | Correct | PASS |
| t-closeness | EMD calculation | Correct | PASS |
| Risk Score | Equal weights | Weighted (0.5,0.3,0.2) | Different |

### Architectural Gap

| Aspect | SDS | Actual |
|--------|-----|--------|
| Input Source | RabbitMQ queue | HTTP POST |
| Policy Source | PostgreSQL | HTTP request body |
| Output | Queue + DB write | HTTP response |
| Audit Events | Required | Missing |

---

## 5. Chat/Orchestrator Gaps

### Fundamental Design Shift

| Aspect | SDS Orchestrator | Chat-Service |
|--------|-----------------|--------------|
| Model | Job-based lifecycle | Session-based chat |
| Storage | PostgreSQL | Redis (volatile) |
| Approval | Explicit endpoints | Text detection |
| NLP | Separate spaCy service | LLM (Qwen2.5:14b) |
| User Management | JWT + RBAC | None |

### Missing Features

- User authentication/authorization
- Job persistence (PostgreSQL)
- Explicit approval workflow
- Federation initiation
- Audit event publishing

---

## 6. Data Design Gaps

### Database Tables

| Table | SDS | Actual | Status |
|-------|-----|--------|--------|
| users | Required | Missing | CRITICAL |
| policies | Required | Missing | CRITICAL |
| policy_rules | Required | Missing | CRITICAL |
| audit_logs | Required | Missing | CRITICAL |
| nlp_annotations | Required | Missing | HIGH |
| masking_results | Required | Missing | HIGH |
| jobs | 23 fields | 9 fields | PARTIAL |
| validations | Required | Exists | OK |
| regulations | Required | Exists | OK |

### Storage Phases

| Phase | SDS Purpose | Actual | Gap |
|-------|-------------|--------|-----|
| intake/ | Upload validation | No validation | CRITICAL |
| staging/ | Processing | Exists | OK |
| quarantine/ | Failed files | Missing | CRITICAL |
| safe/ | Approved output | /storage/output | PARTIAL |
| archive/ | 7-year retention | Missing | CRITICAL |

---

## 7. Priority Remediation Roadmap

### Phase 1: Critical (Production Blockers)

| Priority | Task | Impact |
|----------|------|--------|
| 1 | Fix CORS (remove wildcard) | Security |
| 2 | Add JWT authentication | Security |
| 3 | Implement Audit Service | Compliance |
| 4 | Add encryption (AES-256) | Compliance |
| 5 | Integrate HashiCorp Vault | Security |
| 6 | Fix path traversal vulnerability | Security |
| 7 | Remove exposed DB ports | Security |

### Phase 2: High (Functional Gaps)

| Priority | Task | Impact |
|----------|------|--------|
| 8 | Implement RabbitMQ queues | Architecture |
| 9 | Add Storage Service (MinIO) | Architecture |
| 10 | Add quarantine/archive phases | Compliance |
| 11 | Fix masking execution order | Functionality |
| 12 | Add missing generalization levels | Functionality |
| 13 | Implement patient-level date shifting | Functionality |

### Phase 3: Medium (Enhancements)

| Priority | Task |
|----------|------|
| 14 | Add Prometheus monitoring |
| 15 | Implement structured logging |
| 16 | Add Federation Gateway |
| 17 | Support multi-format files |
| 18 | Add retry/DLQ logic |

---

## 8. Summary Scorecard

| Category | Score | Status |
|----------|-------|--------|
| Services (7 required) | 4/7 | 57% - 3 MISSING |
| Security Controls | 2/12 | 17% - CRITICAL |
| Database Tables | 9/17 | 53% - 8 MISSING |
| Privacy Metrics | 4/4 | 100% - COMPLETE |
| Masking Techniques | 5/5 | 100% - EXISTS (bugs) |
| Regulatory Compliance | 3/8 | 35% - HIGH RISK |
| Monitoring/Logging | 0/6 | 0% - NONE |
| Federation Capability | 0/1 | 0% - MISSING |
| **OVERALL** | ~40% | NOT PRODUCTION-READY |

---

## 9. Conclusion

The SADNxAI implementation represents a **functional MVP** with core anonymization capabilities (masking, validation) working correctly. However, it deviates significantly from the SDS enterprise architecture:

**What Works Well:**
- Privacy metrics (k-anonymity, l-diversity, t-closeness)
- 5 masking techniques implemented
- PDF report generation
- LLM-based conversational interface

**Critical Gaps for Production:**
- Zero security controls (auth, encryption, CORS)
- No audit trail (PDPL non-compliance)
- Missing 3 core services (Storage, Audit, Federation)
- No message queue architecture
- No secret management (Vault)

**Estimated Effort to SDS Compliance:**
- Critical fixes: 4-6 weeks
- Full compliance: 10-14 weeks

---

*Generated: 2026-01-08*
