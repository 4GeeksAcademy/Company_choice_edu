from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    Incident,
    IncidentArea,
    IncidentAuditEvent,
    IncidentCreate,
    IncidentSeverity,
    IncidentStatus,
    IncidentUpdate,
)


class IncidentStore:
    def __init__(self) -> None:
        self._incidents: dict[str, Incident] = {}
        self._audit_events: dict[str, list[IncidentAuditEvent]] = {}

    def create(self, payload: IncidentCreate) -> Incident:
        now = datetime.now(timezone.utc)
        incident = Incident(
            id=str(uuid4()),
            title=payload.title,
            description=payload.description,
            type=payload.type,
            severity=payload.severity,
            channel=payload.channel,
            status=IncidentStatus.new,
            responsible_area=payload.responsible_area,
            created_at=now,
            updated_at=now,
        )
        self._incidents[incident.id] = incident
        self._audit_events[incident.id] = []
        return incident

    def get(self, incident_id: str) -> Incident | None:
        return self._incidents.get(incident_id)

    def update(self, incident_id: str, payload: IncidentUpdate) -> Incident | None:
        incident = self.get(incident_id)
        if incident is None:
            return None
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(incident, field, value)
        incident.updated_at = datetime.now(timezone.utc)
        return incident

    def list_all(
        self,
        status: IncidentStatus | None = None,
        severity: IncidentSeverity | None = None,
        responsible_area: IncidentArea | None = None,
    ) -> list[Incident]:
        incidents = list(self._incidents.values())
        return [
            incident
            for incident in incidents
            if (status is None or incident.status == status)
            and (severity is None or incident.severity == severity)
            and (
                responsible_area is None
                or incident.responsible_area == responsible_area
            )
        ]

    def open_by_severity(self) -> dict[IncidentSeverity, int]:
        summary = {severity: 0 for severity in IncidentSeverity}
        for incident in self._incidents.values():
            if incident.status != IncidentStatus.closed:
                summary[incident.severity] += 1
        return summary

    def update_status(
        self, incident_id: str, status: IncidentStatus, changed_by: str
    ) -> Incident | None:
        incident = self.get(incident_id)
        if incident is None:
            return None
        previous_value = incident.status.value
        incident.status = status
        self._record_change(incident, "status", previous_value, status.value, changed_by)
        return incident

    def update_area(
        self, incident_id: str, area: IncidentArea, changed_by: str
    ) -> Incident | None:
        incident = self.get(incident_id)
        if incident is None:
            return None
        previous_value = incident.responsible_area.value if incident.responsible_area else None
        incident.responsible_area = area
        self._record_change(incident, "responsible_area", previous_value, area.value, changed_by)
        return incident

    def audit(self, incident_id: str) -> list[IncidentAuditEvent] | None:
        if incident_id not in self._incidents:
            return None
        return self._audit_events[incident_id]

    def _record_change(
        self,
        incident: Incident,
        field: str,
        previous_value: str | None,
        new_value: str,
        changed_by: str,
    ) -> None:
        now = datetime.now(timezone.utc)
        incident.updated_at = now
        self._audit_events[incident.id].append(
            IncidentAuditEvent(
                id=str(uuid4()),
                incident_id=incident.id,
                field=field,
                previous_value=previous_value,
                new_value=new_value,
                changed_by=changed_by,
                changed_at=now,
            )
        )