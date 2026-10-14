import { getOpenIncidentSummary, type IncidentSeveritySummary } from "@repo/shared-types";

export const dynamic = "force-dynamic";

const labels = { critical: "Críticas", high: "Altas", medium: "Medias", low: "Bajas" } as const;

async function loadSummary(): Promise<{ data: IncidentSeveritySummary; online: boolean }> {
  try {
    const data = await getOpenIncidentSummary(process.env.INCIDENT_API_URL ?? "http://127.0.0.1:8000");
    return { data, online: true };
  } catch {
    return { data: { critical: 0, high: 0, medium: 0, low: 0 }, online: false };
  }
}

export default async function BackofficeHome() {
  const { data, online } = await loadSummary();
  const total = Object.values(data).reduce((sum, value) => sum + value, 0);
  return <div className="shell">
    <aside><div className="mark">HC</div><strong>HealthCore<br />Operations</strong><nav><a className="active" href="/">Panel</a><a href="#incidents">Incidencias</a><a href="#modules">Módulos</a></nav><small>Uso interno · Sin PHI</small></aside>
    <main><header><div><p className="eyebrow">Centro de operaciones</p><h1>Buenos días, equipo.</h1><p className="subtitle">Una vista clara del trabajo que requiere atención.</p></div><span className={online ? "status online" : "status"}>{online ? "API conectada" : "API no disponible"}</span></header>
      <section className="overview" id="incidents"><div className="overview-title"><p>Incidencias abiertas</p><strong>{total}</strong></div><div className="severity-grid">{Object.entries(data).map(([severity, count]) => <div key={severity} className={`severity ${severity}`}><span>{labels[severity as keyof typeof labels]}</span><strong>{count}</strong></div>)}</div></section>
      <section className="modules" id="modules"><div><p className="eyebrow">Espacio preparado</p><h2>Módulos operativos</h2></div><div className="module-list"><article><span>01</span><div><h3>Gestión de incidencias</h3><p>Clasificación, asignación y auditoría por área responsable.</p></div><b>Activo</b></article><article><span>02</span><div><h3>Inventario clínico</h3><p>Stock derivado, lotes y alertas de reorden por clínica.</p></div><b>Preparado</b></article></div></section>
    </main>
  </div>;
}