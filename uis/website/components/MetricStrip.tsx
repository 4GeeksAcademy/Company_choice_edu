const metrics = [
  ["12", "clínicas"],
  ["2", "países"],
  ["200", "profesionales"],
  ["Mismo día", "citas disponibles"],
] as const;

export function MetricStrip() {
  return <section className="metrics" aria-label="HealthCore en cifras">{metrics.map(([value, label]) => <div key={label}><strong>{value}</strong><span>{label}</span></div>)}</section>;
}