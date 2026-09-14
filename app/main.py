from fastapi import FastAPI

from app.database import Base, engine

from app.routers import projects
from app.routers import experiments
from app.routers import metrics


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Experiment Hub",
    description="Track machine learning experiments and metrics.",
    version="0.1.0",
)


app.include_router(projects.router)
app.include_router(experiments.router)
app.include_router(metrics.router)


@app.get("/")
def root():
    return {
        "name": "AI Experiment Hub",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }