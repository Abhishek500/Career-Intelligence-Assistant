from fastapi import FastAPI

from app.api import resume, job, compare, compare_v2, compare_v3

app = FastAPI(title="Career Intelligence Assistant")

# Phase 1 endpoints
app.include_router(resume.router)
app.include_router(job.router)
app.include_router(compare.router)

# Phase 2 endpoints
app.include_router(compare_v2.router)
app.include_router(compare_v3.router)
