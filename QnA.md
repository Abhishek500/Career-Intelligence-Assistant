## 1) What would be required to productionize your solution, make it scalable and deploy it on a hyper-scaler such as AWS / GCP / Azure?

To take this system to production, I would first containerize it so it can run consistently across environments. The API should be stateless so multiple instances can run in parallel behind a load balancer.

For scale, resume uploads and LLM-based extraction should be handled asynchronously. The API can accept the upload, return a request ID, and process the heavy work in the background. This keeps the system responsive as usage grows.

As the system matures, I would add persistent storage for resumes, extracted data, and results, along with basic monitoring for errors and latency.

---

## 2) RAG/LLM approach & decisions: Choices considered and final choice for LLM / embedding model / vector database / orchestration framework, prompt & context management, guardrails, quality, observability

LLMs are used only where language understanding and reasoning are required, such as extracting structured information from resumes and identifying transferable skills.

The core scoring and matching logic is fully deterministic and rule-based. This ensures results are consistent, explainable, and easy to debug, and avoids relying on probabilistic model outputs for critical decisions.

For this phase, RAG is intentionally not used because the required information already exists within the resume or job description. The challenge is structuring and normalizing the data, not retrieving external knowledge.

LLM outputs are constrained using well-defined prompts and validated against typed schemas to ensure predictable structure. Guardrails are in place to handle malformed outputs safely rather than failing the pipeline.

This separation allows the system to benefit from LLM flexibility while maintaining reliability, auditability, and control over final outcomes.


---

## 3) Key technical decisions you made and why

A key decision was to build a deterministic baseline before adding LLM-based reasoning. This provides a stable foundation and makes the system easier to evaluate.

Another important decision was enforcing structured outputs using typed schemas, which reduces integration errors and improves reliability.

Finally, extracted reasoning is reused across the pipeline instead of being recomputed, improving both consistency and performance.

---

## 4) Engineering standards you’ve followed (and maybe some that you skipped)

I followed best practices such as separation of concerns, clear module boundaries, and explicit data contracts between components.

For this MVP, I intentionally skipped features like authentication, full observability, and large-scale persistence. These are important for production but not required at this stage.

This trade-off allowed faster development while keeping the design clean and extensible.

---

## 5) How you used AI tools in your development process

AI tools (Windsurf and ChatGPT) were used to speed up development, mainly for code scaffolding, prompt iteration, and debugging issues during implementation.

All critical logic—such as scoring, matching, and overall system architecture—was designed and controlled manually to keep the system understandable, auditable, and deterministic.

Key design choices made deliberately by me include:
- Using **Pydantic schemas** to define clear, typed contracts between components and to validate LLM outputs.
- Separating the **API layer from core business logic**, keeping the API thin and making the core logic reusable, testable, and independent of any framework.
- Choosing a **deterministic-first approach** for scoring and alignment, with LLMs used only where language reasoning is required.
- Designing the system so extracted reasoning is stored and reused, rather than recomputed, to ensure consistency.

Overall, AI tools accelerated iteration, but architectural decisions and correctness guarantees were explicitly engineered rather than generated.

---

## 6) What you'd do differently with more time

With more time, I would add persistent storage and background job processing to make the system production-ready.

I would also introduce an evaluation framework to measure extraction quality and scoring accuracy over time.

Finally, I would improve logging and monitoring so system behavior can be easily inspected in real-world usage.
```
