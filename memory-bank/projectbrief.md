# Resumen del proyecto

HealthCore opera 12 clínicas en Estados Unidos y Reino Unido. El producto reduce la fragmentación operativa mediante un sitio público coherente y un backoffice para incidencias e inventario, respetando HIPAA y UK GDPR.

## Objetivos

- Mantener en `uis/website` la presencia corporativa y el acceso a las clínicas.
- Mostrar en `uis/backoffice` información operativa obtenida desde servicios reales.
- Reutilizar contratos de `packages/shared` sin copiar lógica entre aplicaciones.
- Preparar módulos trazables para las 12 clínicas sin procesar PHI en este MVP.

El resumen de incidencias abiertas conecta el backoffice con la operación. Los KPI empresariales de referencia, como el 22% de no-shows y el 14% de reclamaciones rechazadas descritos en `CONTEXT.md`, quedan fuera del alcance funcional actual y no deben presentarse como datos en tiempo real.