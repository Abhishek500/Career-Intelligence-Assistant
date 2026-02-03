# Answers to the reviewer questions

## 1) What is required to productionize and scale on AWS/GCP/Azure?

**Compute and runtime**

- Run as a containerized service (Docker) behind:
  - AWS: ALB + ECS/Fargate or EKS
  - GCP: Cloud Run or GKE
  - Azure: Container Apps or AKS

**State/storage**

- Replace in-memory stores with persistent storage:
  - Relational: Postgres (jobs, candidates, results)
  - Object storage: S3/GCS/Azure Blob (raw resumes)

**Async processing**

- Move resume extraction to a background job queue (Celery/RQ/Cloud Tasks/SQS):
  - API accepts upload → returns `candidate_id` and `status=pending`
  - Worker performs extraction → updates DB

**Scaling strategy**

- Horizontally scale the API (stateless)
- Separate worker pool for LLM-heavy workloads
- Apply concurrency limits for LLM calls

**Reliability**

- Retries with exponential backoff on transient LLM failures
- Circuit breakers / rate limiting
- Idempotency keys for resume uploads

**Security**

- AuthN/AuthZ (JWT/OAuth)
- Input validation + malware scanning for uploads
- Secret management (AWS Secrets Manager / GCP Secret Manager / Azure Key Vault)

**Observability**

- Structured logging + tracing (OpenTelemetry)
- Metrics (latency, error rates, LLM token usage, parse-failure rates)
- Persist reasoning traces for audits

---

## 2) RAG/LLM approach & decisions

**Where LLM is used (intentionally constrained)**

- Transferable skill inference (`TransferableSkillEngine`)
- Resume extraction to structured schema (`ResumeExtractionPipeline`)
- Alignment explanation Q&A (LLM explains *provided facts only*)

**Where LLM is not used**

- Baseline scoring and matching
- Alignment fact computation (`compute_alignment`)

**Why RAG is not used in Phase 3 resume extraction**

- The information is already present in the resume; the problem is *structure/normalization*, not retrieval.

**If adding RAG later (recommended scope)**

- Use RAG for:
  - Job taxonomy enrichment (skill ontology)
  - Learning resources recommendations
  - Cross-role similarity search
  - Company/domain context augmentation

**Embedding model / vector DB / orchestration (future production choice)**

- Embeddings:
  - OpenAI `text-embedding-3-small` or `text-embedding-3-large`, or a local option like `bge-small` depending on cost/security
- Vector DB:
  - Managed: Pinecone / Weaviate Cloud / Vertex Vector Search
  - Self-managed: pgvector (simple + strong operational story)
- Orchestration:
  - Keep your current “LLM client + prompts + typed schemas” pattern
  - If you need multi-step chains: LangGraph or a minimal custom orchestrator

**Prompt/context management**

- Prompts are explicit and schema-driven
- Context passed to LLM is bounded and deterministic (alignment_context)
- JSON repair logic exists because real LLM outputs are not always valid JSON

**Guardrails**

- Schema validation (Pydantic)
- Explicit “facts only” rules in Q&A prompt
- Fallbacks to safe defaults to avoid crashing the pipeline

**Quality & observability**

- Track:
  - JSON parse success rate
  - frequency of repairs
  - frequency of fallbacks
  - LLM latency and token usage

---

## 3) Key technical decisions and why

- **Deterministic-first baseline**
  - gives a stable floor for correctness and debuggability

- **LLM used for reasoning/extraction, not for scoring math**
  - keeps output reproducible and auditable

- **Typed contracts via Pydantic**
  - makes integration boundaries explicit and testable

- **Store transferables and reuse them in Q&A**
  - avoids recomputing and ensures Q&A reflects the evaluated reasoning

- **JSON repair instead of hard-failing**
  - production systems must handle non-ideal LLM behavior

---

## 4) Engineering standards followed (and intentionally skipped)

**Followed**

- Separation of concerns (API thin, core logic in modules)
- Typed schemas / contracts
- Deterministic baseline and deterministic alignment context
- Guardrails against invalid LLM outputs

**Skipped (MVP trade-offs)**

- Persistent storage
- Auth
- End-to-end automated evaluation suite
- Full tracing/metrics pipeline

---

## 5) How AI tools were used

- Prompt iteration (making JSON output more reliable)
- Debugging assistance (identifying failure modes like truncation, unclosed braces)
- Refactoring help (moving toward modular “phase” abstractions)

The key constraint: AI tools were used to accelerate iteration, but the core scoring and system boundaries were kept deliberate and inspectable.

---

## 6) What I would do differently with more time

- Make resume extraction asynchronous + persistent (queue + DB)
- Add a robust evaluation harness:
  - golden datasets
  - regression tests for JSON repair
  - scoring calibration
- Replace prints with structured logging + log levels
- Migrate from deprecated `google.generativeai` to `google.genai`
- Add authentication + multi-tenant isolation
- Add a UI to demonstrate the reasoning trace and Q&A

---