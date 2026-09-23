from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class IncidentType(str, Enum):
    clinical_operations = "clinical-operations"
    patient_access = "patient-access"
    billing_revenue = "billing-revenue"
    compliance_data = "compliance-data"
    workforce = "workforce"
    technology = "technology"


class IncidentSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class IncidentChannel(str, Enum):
    phone = "phone"
    email = "email"
    internal_message = "internal-message"
    monitoring = "monitoring"
    in_person = "in-person"
    manual_entry = "manual-entry"


class IncidentStatus(str, Enum):
    new = "new"
    triaged = "triaged"
    assigned = "assigned"
    in_progress = "in-progress"
    blocked = "blocked"
    resolved = "resolved"
    closed = "closed"


class IncidentArea(str, Enum):
    clinical_operations = "clinical-operations"
    patient_access = "patient-access"
    billing_revenue = "billing-revenue"
    compliance_data = "compliance-data"
    workforce = "workforce"
    technology = "technology"
    executive = "executive"


class IncidentCreate(BaseModel):
    title: str
    description: str
    type: IncidentType
    severity: IncidentSeverity
    channel: IncidentChannel
    responsible_area: IncidentArea | None = None


class Incident(BaseModel):
    id: str
    title: str
    description: str
    type: IncidentType
    severity: IncidentSeverity
    channel: IncidentChannel
    status: IncidentStatus
    responsible_area: IncidentArea | None
    created_at: datetime
    updated_at: datetime


class IncidentAuditEvent(BaseModel):
    id: str
    incident_id: str
    field: str
    previous_value: str | None
    new_value: str
    changed_by: str
    changed_at: datetime


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
    changed_by: str


class IncidentAreaUpdate(BaseModel):
    responsible_area: IncidentArea
    changed_by: str