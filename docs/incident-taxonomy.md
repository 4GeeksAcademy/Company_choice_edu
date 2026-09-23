# Taxonomía propuesta de incidencias

Esta taxonomía se define para el primer gestor de incidencias de HealthCore. Los valores no estaban incluidos en `CONTEXT.md`; son una decisión de producto basada en los departamentos, riesgos y problemas descritos allí.

## Tipos de incidencia

- `clinical-operations`: problemas de atención clínica, sedes, citas clínicas o sistemas EHR.
- `patient-access`: problemas de acceso, reservas, recordatorios o experiencia del paciente.
- `billing-revenue`: problemas de reclamaciones, facturación, cobros o rechazos.
- `compliance-data`: problemas de privacidad, acceso a datos, auditoría o cumplimiento.
- `workforce`: problemas de personal, onboarding, formación o credenciales.
- `technology`: fallos de aplicaciones, integraciones, infraestructura o monitorización.

## Severidades

- `critical`: riesgo para la seguridad del paciente, posible incumplimiento grave o caída generalizada sin alternativa.
- `high`: impacto importante en varias sedes, un proceso esencial o una obligación regulatoria, con alternativa limitada.
- `medium`: impacto relevante pero limitado a un equipo, una sede o un proceso con alternativa disponible.
- `low`: impacto menor, consulta operativa o problema sin interrupción significativa.

## Canales de entrada

- `phone`: llamada telefónica de una clínica o equipo operativo.
- `email`: correo electrónico.
- `internal-message`: mensaje de un canal interno.
- `monitoring`: alerta automática de monitorización.
- `in-person`: comunicación presencial.
- `manual-entry`: registro manual realizado por Operaciones.

## Estados

- `new`: registrada, todavía no revisada.
- `triaged`: revisada y clasificada.
- `assigned`: tiene un área responsable.
- `in-progress`: el área responsable está trabajando en ella.
- `blocked`: no puede avanzar por una dependencia o falta de información.
- `resolved`: se aplicó una solución y queda pendiente de confirmación.
- `closed`: la resolución fue confirmada y no quedan acciones pendientes.

## Áreas responsables

Las áreas proceden del contexto de HealthCore:

- Operaciones Clínicas.
- Experiencia del Paciente y Acceso.
- Ciclo de Ingresos y Facturación.
- Cumplimiento y Gobierno del Dato.
- Personas y Fuerza Laboral.
- Tecnología.
- Dirección Ejecutiva.

## Reglas de trazabilidad

- Toda incidencia se crea con tipo, severidad, canal, estado inicial y área responsable cuando ya sea posible asignarla.
- Los cambios de estado y de área responsable se registran como eventos inmutables.
- Cada evento conserva la incidencia afectada, el valor anterior, el valor nuevo, el usuario que realizó el cambio y la fecha y hora.
- Una incidencia cerrada no se elimina; si reaparece el problema, se registra una nueva incidencia relacionada.