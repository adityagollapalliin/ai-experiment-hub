from fastapi import FastAPI

app = FastAPI(
    title="AI Experiment Hub",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "name": "AI Experiment Hub",
        "status": "running"
    }