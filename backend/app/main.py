from datetime import datetime, timezone

from fastapi import FastAPI
from backend.app.tools.excel_analyzer import router as excel_router

app = FastAPI(
    title="Excel-sun-IA",
    description="Especialista em Excel, Power BI e Google Sheets",
    version="0.2.0"
)

app.include_router(excel_router)

@app.get("/")
def home():
    return {
        "project": "Excel-sun-IA",
        "status": "online",
        "message": "Agente de dados inicializado"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
