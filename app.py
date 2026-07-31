from __future__ import annotations

from fastapi import FastAPI
from dotenv import load_dotenv

from config.settings import settings
from models.signals import build_signal
from services.graph_client import GraphClient
from services.openai_service import generate_risk_summary
from services.risk_engine import summarize_risk

load_dotenv()

app = FastAPI(title="TempoPilot API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "TempoPilot API"}


@app.get("/api/project-risk")
def project_risk(project_name: str = "Sample Project"):
    graph = GraphClient(settings)
    signals = build_signal(project_name=project_name, **graph.list_project_signals())
    risk = summarize_risk(signals)

    try:
        risk["explanation"] = generate_risk_summary(project_name, signals, risk["risk_score"])
    except ValueError:
        risk["explanation"] = (
            "AI summary unavailable. Please confirm Azure OpenAI configuration in the environment settings."
        )

    return risk


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
