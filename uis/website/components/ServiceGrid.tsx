const services = [
  ["Atención primaria", "Seguimiento cercano para cada etapa de la vida."],
  ["Especialistas", "Derivaciones coordinadas sin perder continuidad."],
  ["Salud preventiva", "Revisiones y programas para anticiparse al riesgo."],
  ["Cuidado crónico", "Planes claros y acompañamiento entre consultas."],
] as const;

export function ServiceGrid() {
  return <div className="service-grid">{services.map(([title, copy], index) => <article key={title}><span>0{index + 1}</span><h3>{title}</h3><p>{copy}</p></article>)}</div>;
}