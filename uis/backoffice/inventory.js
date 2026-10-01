const API_URL = location.hostname.includes("github.dev")
  ? `${location.protocol}//${location.hostname.replace(/-\d+(?=\.)/, "-8000")}`
  : "http://localhost:8000";
let items = [];

const api = (path, options = {}) => fetch(`${API_URL}${path}`, { ...options, headers: { "Content-Type": "application/json", ...options.headers } });
const formData = (form) => Object.fromEntries(new FormData(form).entries());

async function loadItems() {
  const response = await api("/inventory/items");
  items = response.ok ? await response.json() : [];
  const clinics = [...new Set(items.map((item) => item.clinic_location))];
  const filter = document.querySelector("#clinic-filter");
  const selected = filter.value;
  filter.innerHTML = `<option value="">Todas</option>${clinics.map((clinic) => `<option>${clinic}</option>`).join("")}`;
  filter.value = selected;
  document.querySelectorAll(".item-select").forEach((select) => {
    select.innerHTML = items.map((item) => `<option value="${item.id}">${item.name} · ${item.clinic_location}</option>`).join("");
  });
  render();
}

function render() {
  const clinic = document.querySelector("#clinic-filter").value;
  const onlyLow = document.querySelector("#reorder-filter").checked;
  const visible = items.filter((item) => (!clinic || item.clinic_location === clinic) && (!onlyLow || item.below_reorder));
  document.querySelector("#item-count").textContent = visible.length;
  document.querySelector("#reorder-count").textContent = visible.filter((item) => item.below_reorder).length;
  document.querySelector("#inventory-list").innerHTML = visible.map((item) => `<tr data-id="${item.id}"><td>${item.name}</td><td>${item.clinic_location}</td><td>${item.category}</td><td>${item.available_stock}</td><td>${item.reorder_point}</td><td class="${item.below_reorder ? "status-low" : ""}">${item.below_reorder ? "Reordenar" : "Disponible"}</td></tr>`).join("") || `<tr><td colspan="6">Sin resultados</td></tr>`;
  document.querySelectorAll("[data-id]").forEach((row) => row.addEventListener("click", () => showDetail(row.dataset.id)));
}

async function showDetail(itemId) {
  const [lotsResponse, movementsResponse] = await Promise.all([api(`/inventory/items/${itemId}/lots`), api(`/inventory/items/${itemId}/movements`)]);
  const lots = lotsResponse.ok ? await lotsResponse.json() : [];
  const movements = movementsResponse.ok ? await movementsResponse.json() : [];
  document.querySelector("#inventory-detail").textContent = `Lotes: ${lots.map((lot) => lot.lot_code).join(", ") || "ninguno"}. Movimientos: ${movements.length}.`;
  const lotSelect = document.querySelector("#movement-form [name=lot_id]");
  lotSelect.innerHTML = `<option value="">Sin lote</option>${lots.map((lot) => `<option value="${lot.id}">${lot.lot_code}</option>`).join("")}`;
}

async function submit(form, path, transform = (data) => data) {
  const response = await api(path, { method: "POST", body: JSON.stringify(transform(formData(form))) });
  const message = document.querySelector("#inventory-message");
  message.textContent = response.ok ? "Operación registrada." : (await response.json()).detail || "No se pudo registrar.";
  if (response.ok) { form.reset(); await loadItems(); }
}

document.querySelector("#item-form").addEventListener("submit", (event) => { event.preventDefault(); submit(event.currentTarget, "/inventory/items", (data) => ({ ...data, reorder_point: Number(data.reorder_point) })); });
document.querySelector("#lot-form").addEventListener("submit", (event) => { event.preventDefault(); submit(event.currentTarget, "/inventory/lots", (data) => ({ ...data, received_at: new Date().toISOString() })); });
document.querySelector("#movement-form").addEventListener("submit", (event) => { event.preventDefault(); submit(event.currentTarget, "/inventory/movements", (data) => ({ ...data, lot_id: data.lot_id || null, quantity: Number(data.quantity), reason: data.reason || null })); });
document.querySelector("#clinic-filter").addEventListener("change", render);
document.querySelector("#reorder-filter").addEventListener("change", render);
loadItems();