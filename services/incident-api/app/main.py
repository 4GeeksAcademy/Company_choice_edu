from fastapi import FastAPI


app = FastAPI(
    title="HealthCore Incident API",
    version="0.1.0",
    description="API for the centralized operational incident manager.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}