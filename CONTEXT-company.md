# Contexto del gestor de incidencias de HealthCore

Este documento complementa `CONTEXT.md` con las decisiones de producto específicas del gestor centralizado de incidencias.

## Usuarios

El backoffice lo utiliza el equipo de Operaciones de HealthCore para registrar problemas procedentes de las 12 clínicas y asignarlos al área que debe resolverlos.

## Campos de una incidencia

- `title`: resumen breve del problema.
- `description`: impacto e información disponible.
- `type`: clasificación funcional.
- `severity`: nivel de impacto.
- `channel`: canal por el que se recibió.
- `responsible_area`: área responsable, opcional durante el alta.
- `status`: estado del ciclo de vida.

## Tipos

- `clinical-operations`
- `patient-access`
- `billing-revenue`
- `compliance-data`
- `workforce`
- `technology`

## Severidades

- `critical`
- `high`
- `medium`
- `low`

## Canales de entrada

- `phone`
- `email`
- `internal-message`
- `monitoring`
- `in-person`
- `manual-entry`

## Áreas responsables

- `clinical-operations`
- `patient-access`
- `billing-revenue`
- `compliance-data`
- `workforce`
- `technology`
- `executive`

## Ciclo de vida

- `new`
- `triaged`
- `assigned`
- `in-progress`
- `blocked`
- `resolved`
- `closed`

El estado `reopened` no forma parte de este contexto. Si un problema cerrado reaparece, se crea una incidencia nueva relacionada.

## Auditoría

Cada cambio de `status` o `responsible_area` conserva el valor anterior, el valor nuevo, el autor y la fecha y hora UTC. El historial se consulta desde el detalle de la incidencia.

## Datos de muestra

El MVP no carga datos de semilla. Las incidencias se crean desde la interfaz o la API y se almacenan en memoria durante la ejecución.