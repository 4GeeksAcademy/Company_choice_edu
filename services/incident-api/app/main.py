from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    Incident,
    IncidentAreaUpdate,
    IncidentAuditEvent,
    IncidentCreate,
    IncidentStatusUpdate,
)
from .store import IncidentStore


app = FastAPI(
    title="HealthCore Incident API",
    version="0.1.0",
    description="API for the centralized operational incident manager.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = IncidentStore()


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/incidents", response_model=Incident, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate) -> Incident:
    return store.create(payload)


@app.get("/incidents", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return store.list_all()


@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str) -> Incident:
    incident = store.get(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.patch("/incidents/{incident_id}/status", response_model=Incident)
def update_incident_status(
    incident_id: str, payload: IncidentStatusUpdate
) -> Incident:
    incident = store.update_status(incident_id, payload.status, payload.changed_by)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.patch("/incidents/{incident_id}/responsible-area", response_model=Incident)
def update_incident_area(
    incident_id: str, payload: IncidentAreaUpdate
) -> Incident:
    incident = store.update_area(
        incident_id, payload.responsible_area, payload.changed_by
    )
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.get(
    "/incidents/{incident_id}/audit",
    response_model=list[IncidentAuditEvent],
)
def get_incident_audit(incident_id: str) -> list[IncidentAuditEvent]:
    events = store.audit(incident_id)
    if events is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return events