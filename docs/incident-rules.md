# Reglas iniciales del gestor de incidencias

## Reglas confirmadas

- El gestor centraliza incidencias operativas de HealthCore.
- Una incidencia debe poder registrarse aunque llegue desde canales diferentes.
- Una incidencia debe poder clasificarse y asignarse a un área responsable.
- Una incidencia debe tener un estado consultable.
- Cada cambio de estado debe registrar quién lo realizó y cuándo.
- Cada cambio de responsable debe registrar quién lo realizó y cuándo.
- La solución debe respetar las obligaciones de privacidad y trazabilidad de HIPAA y UK GDPR.
- Las áreas responsables disponibles en el contexto son:
  - Operaciones Clínicas.
  - Experiencia del Paciente y Acceso.
  - Ciclo de Ingresos y Facturación.
  - Cumplimiento y Gobierno del Dato.
  - Personas y Fuerza Laboral.
  - Tecnología.
  - Dirección Ejecutiva.

## Decisiones pendientes

El `CONTEXT.md` actual no especifica todavía los valores válidos para:

- Tipos de incidencia.
- Niveles de severidad.
- Canales de entrada.
- Estados del ciclo de vida.

Estos valores deben confirmarse en el briefing específico del gestor antes de implementar validaciones, formularios o filtros. No se inventan en esta etapa.

## Fuente

- `CONTEXT.md`