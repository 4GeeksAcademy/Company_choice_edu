/** Shared HealthCore contracts consumed across the monorepo. */
export type Id = string;

export interface BaseEntity {
  id: Id;
  createdAt?: string;
  updatedAt?: string;
}

export type IncidentType =
  | "clinical-operations"
  | "patient-access"
  | "billing-revenue"
  | "compliance-data"
  | "workforce"
  | "technology";

export type IncidentSeverity = "critical" | "high" | "medium" | "low";

export type IncidentChannel =
  | "phone"
  | "email"
  | "internal-message"
  | "monitoring"
  | "in-person"
  | "manual-entry";

export type IncidentStatus =
  | "new"
  | "triaged"
  | "assigned"
  | "in-progress"
  | "blocked"
  | "resolved"
  | "closed";

export type IncidentArea =
  | "clinical-operations"
  | "patient-access"
  | "billing-revenue"
  | "compliance-data"
  | "workforce"
  | "technology"
  | "executive";

export interface Incident extends BaseEntity {
  title: string;
  description: string;
  type: IncidentType;
  severity: IncidentSeverity;
  channel: IncidentChannel;
  status: IncidentStatus;
  responsibleArea?: IncidentArea;
}

export interface IncidentAuditEvent {
  id: Id;
  incidentId: Id;
  field: "status" | "responsibleArea";
  previousValue: string | null;
  newValue: string;
  changedBy: Id;
  changedAt: string;
}

export type IncidentSeveritySummary = Record<IncidentSeverity, number>;

export async function getOpenIncidentSummary(
  apiUrl: string,
): Promise<IncidentSeveritySummary> {
  const response = await fetch(`${apiUrl}/incidents/summary/open-by-severity`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Incident summary is unavailable");
  }

  return response.json() as Promise<IncidentSeveritySummary>;
}

export type InventoryUnit = "unit" | "box" | "ml" | "tablet";
export type InventoryCategory =
  | "ppe"
  | "medical_consumables"
  | "otc_medication"
  | "clinical_equipment";
export type InventoryCountry = "us" | "uk";
export type InventoryMovementType = "inbound" | "outbound" | "adjustment";

export interface InventoryItem extends BaseEntity {
  clinicLocation: string;
  country: InventoryCountry;
  name: string;
  category: InventoryCategory;
  unitOfMeasure: InventoryUnit;
  reorderPoint: number;
  availableStock: number;
  belowReorder: boolean;
}

export interface InventoryLot {
  id: Id;
  itemId: Id;
  lotCode: string;
  expiryDate: string;
  receivedAt: string;
}

export interface InventoryMovement {
  id: Id;
  itemId: Id;
  lotId?: Id;
  movementType: InventoryMovementType;
  quantity: number;
  reason?: string;
  createdAt: string;
}
