const API_URL = "http://localhost:8000";
let incidents = [];

const labels = {
  status: { new: "Nueva", triaged: "Clasificada", assigned: "Asignada", "in-progress": "En progreso", blocked: "Bloqueada", resolved: "Resuelta", closed: "Cerrada" },
  severity: { critical: "Crítica", high: "Alta", medium: "Media", low: "Baja" },
  type: { technology: "Tecnología", "clinical-operations": "Operaciones clínicas", "patient-access": "Acceso del paciente", "billing-revenue": "Facturación e ingresos", "compliance-data": "Cumplimiento y datos", workforce: "Personas y fuerza laboral" },
};

const listElement = document.querySelector("#incident-list");
const form = document.querySelector("#incident-form");
const message = document.querySelector("#form-message");

async function loadIncidents() {
  try {
    const response = await fetch(`${API_URL}/incidents`);
    if (!response.ok) throw new Error("No se pudo cargar la cola");
    incidents = await response.json();
    renderMetrics();
    renderList();
  } catch (error) {
    listElement.innerHTML = `<div class="empty-state">No se pudo conectar con la API. Inicia el servicio en el puerto 8000.</div>`;
  }
}

function renderMetrics() {
  document.querySelector("#metric-total").textContent = incidents.length;
  document.querySelector("#nav-count").textContent = incidents.length;
  document.querySelector("#metric-open").textContent = incidents.filter((incident) => incident.status !== "closed").length;
  document.querySelector("#metric-critical").textContent = incidents.filter((incident) => ["critical", "high"].includes(incident.severity) && incident.status !== "closed").length;
  document.querySelector("#metric-resolved").textContent = incidents.filter((incident) => incident.status === "resolved").length;
}

function renderList() {
  const search = document.querySelector("#search-input").value.toLowerCase();
  const status = document.querySelector("#status-filter").value;
  const visible = incidents.filter((incident) => incident.title.toLowerCase().includes(search) && (status === "all" || incident.status === status));
  if (!visible.length) {
    listElement.innerHTML = `<div class="empty-state">No hay incidencias que coincidan con estos filtros.</div>`;
    return;
  }
  listElement.innerHTML = visible.map((incident) => `<button class="incident-row" data-id="${incident.id}" type="button"><span><strong>${escapeHtml(incident.title)}</strong><small>${labels.type[incident.type] || incident.type} · ${formatDate(incident.created_at)}</small></span><span class="badge badge-${incident.severity}">${labels.severity[incident.severity]}</span><span class="badge badge-medium">${labels.status[incident.status]}</span></button>`).join("");
  listElement.querySelectorAll("[data-id]").forEach((row) => row.addEventListener("click", () => showDetail(row.dataset.id)));
}

async function showDetail(id) {
  const incident = incidents.find((item) => item.id === id);
  if (!incident) return;
  const response = await fetch(`${API_URL}/incidents/${id}/audit`);
  const audit = response.ok ? await response.json() : [];
  document.querySelector("#detail-content").innerHTML = `<div class="detail-header"><p class="eyebrow">Detalle de incidencia</p><h3>${escapeHtml(incident.title)}</h3><div class="detail-meta"><span class="badge badge-${incident.severity}">${labels.severity[incident.severity]}</span><span class="badge badge-medium">${labels.status[incident.status]}</span></div></div><p class="detail-label">Descripción</p><p class="detail-description">${escapeHtml(incident.description)}</p><p class="detail-label">Estado</p><select class="detail-select" id="detail-status"><option value="new">Nueva</option><option value="triaged">Clasificada</option><option value="assigned">Asignada</option><option value="in-progress">En progreso</option><option value="blocked">Bloqueada</option><option value="resolved">Resuelta</option><option value="closed">Cerrada</option></select><p class="detail-label">Historial de auditoría</p>${audit.length ? audit.map((event) => `<div class="audit-item"><strong>${event.field === "status" ? "Estado actualizado" : "Área responsable actualizada"}</strong><small>${event.previous_value || "Sin asignar"} → ${event.new_value} · ${event.changed_by}</small></div>`).join("") : `<p class="detail-description">Sin cambios registrados.</p>`}`;
  document.querySelector("#detail-status").value = incident.status;
  document.querySelector("#detail-status").addEventListener("change", (event) => updateStatus(id, event.target.value));
}

async function updateStatus(id, status) {
  await fetch(`${API_URL}/incidents/${id}/status`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status, changed_by: "operations-user" }) });
  await loadIncidents();
  await showDetail(id);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  if (!data.responsible_area) delete data.responsible_area;
  try {
    const response = await fetch(`${API_URL}/incidents`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    if (!response.ok) throw new Error("No se pudo guardar");
    form.reset(); message.textContent = "Incidencia registrada correctamente."; await loadIncidents();
  } catch (error) { message.textContent = "No se pudo registrar. Comprueba que la API esté activa."; }
});

document.querySelector("#search-input").addEventListener("input", renderList);
document.querySelector("#status-filter").addEventListener("change", renderList);
document.querySelector("#new-incident-button").addEventListener("click", () => document.querySelector("#new-incident").scrollIntoView({ behavior: "smooth" }));
document.querySelector("#close-detail").addEventListener("click", () => document.querySelector("#detail-content").innerHTML = `<div class="detail-placeholder"><span>→</span><p>Selecciona una incidencia para revisar sus detalles y trazabilidad.</p></div>`);

function formatDate(value) { return new Date(value).toLocaleDateString("es-ES", { day: "2-digit", month: "short" }); }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#039;", '"': "&quot;" }[character])); }

loadIncidents();