## 1) How would you take this system to production and scale it?

To take this system to production, I would first containerize it so it can run consistently across environments. The API should be stateless so multiple instances can run in parallel behind a load balancer.

For scale, resume uploads and LLM-based extraction should be handled asynchronously. The API can accept the upload, return a request ID, and process the heavy work in the background. This keeps the system responsive as usage grows.

As the system matures, I would add persistent storage for resumes, extracted data, and results, along with basic monitoring for errors and latency.

---

## 2) How are LLMs used in this system, and why did you choose this approach?

LLMs are used only where language understanding and reasoning are required, such as extracting structured information from resumes and identifying transferable skills.

The core scoring and matching logic is deterministic and rule-based. This keeps results consistent, explainable, and easy to debug.

This separation allows the system to benefit from LLM flexibility without sacrificing reliability.

---

## 3) What were the most important technical decisions you made, and why?

A key decision was to build a deterministic baseline before adding LLM-based reasoning. This provides a stable foundation and makes the system easier to evaluate.

Another important decision was enforcing structured outputs using typed schemas, which reduces integration errors and improves reliability.

Finally, extracted reasoning is reused across the pipeline instead of being recomputed, improving both consistency and performance.

---

## 4) What engineering best practices did you follow, and what did you skip for now?

I followed best practices such as separation of concerns, clear module boundaries, and explicit data contracts between components.

For this MVP, I intentionally skipped features like authentication, full observability, and large-scale persistence. These are important for production but not required at this stage.

This trade-off allowed faster development while keeping the design clean and extensible.

---

## 5) How did you use AI tools while building this project?

AI tools were used to speed up development, mainly for prompt iteration, debugging edge cases, and refactoring code.

All critical logic—such as scoring, matching, and decision rules—was designed and controlled manually to keep the system understandable and auditable.

AI assisted the process but did not replace engineering decisions.

---

## 6) If you had more time, what would you improve or add next?

With more time, I would add persistent storage and background job processing to make the system production-ready.

I would also introduce an evaluation framework to measure extraction quality and scoring accuracy over time.

Finally, I would improve logging and monitoring so system behavior can be easily inspected in real-world usage.
```
