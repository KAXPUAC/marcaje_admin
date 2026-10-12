from fastapi import FastAPI
from core.database import init_db_pool
from api.v1.endpoints import liveness

app = FastAPI(title="Universidad Galileo - Reconocimiento Facial API", version="1.0.0")

@app.on_event("startup")
def startup_db_client():
    # Inicializa el Pool de conexiones a Oracle 12c al arrancar
    init_db_pool()

# Registrar Endpoints
app.include_router(liveness.router, prefix="/api/v1/liveness", tags=["Liveness & Marcaje"])

@app.get("/")
def read_root():
    return {"status": "API Online", "system": "Universidad Galileo Biometric"}