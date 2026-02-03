from fastapi import FastAPI
from app.api import resume, job, compare

app = FastAPI(title="Career Intelligence Assistant")

app.include_router(resume.router)
app.include_router(job.router)
app.include_router(compare.router)
