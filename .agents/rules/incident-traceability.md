# Regla: trazabilidad de incidencias

- Modo: siempre.
- Alcance: cambios en `services/incident-api/`, `uis/backoffice/` y contratos compartidos.

## Reglas

- Cada cambio de estado debe guardar campo, valor anterior, valor nuevo, autor y fecha UTC.
- Cada cambio de área responsable debe guardar campo, valor anterior, valor nuevo, autor y fecha UTC.
- Los eventos de historial son consultables desde el detalle de la incidencia.
- No se elimina ni se sobrescribe un evento histórico.
- No se inventan valores de catálogo fuera del contexto o de una decisión documentada.