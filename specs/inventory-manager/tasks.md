# Tareas del gestor de inventario

Cada tarea se implementa y verifica de forma independiente. El mensaje del commit correspondiente debe incluir su ID.

| Estado | Tarea | Criterios | Resultado verificable |
|---|---|---|---|
| [ ] | **INV-T001 — Contratos de dominio** | INV-001, INV-002, INV-004, INV-012 | Modelos Pydantic y tipos compartidos restringen catálogos, cantidades, campos adicionales y texto sensible; sus pruebas de validación pasan. |
| [ ] | **INV-T002 — CRUD de artículos por clínica** | INV-001, INV-011 | API crea, lista, consulta, actualiza y elimina artículos por clínica; rechaza borrar artículos con historial; pruebas CRUD pasan. |
| [ ] | **INV-T003 — Registro de lotes** | INV-002, INV-003, INV-008 | API crea y lista lotes, garantiza unicidad por artículo y valida pertenencia y obligatoriedad; pruebas de lotes pasan. |
| [ ] | **INV-T004 — Libro de movimientos y stock derivado** | INV-004, INV-005 | API registra y lista movimientos y calcula stock sin campo editable; pruebas de entrada, salida y ajuste pasan. |
| [ ] | **INV-T005 — Rechazos atómicos de movimientos** | INV-006, INV-007, INV-008, INV-009 | API rechaza saldo negativo y referencias ausentes, cruzadas o caducadas sin mutar el libro; pruebas de comportamiento no deseado pasan. |
| [ ] | **INV-T006 — Consulta de punto de reorden** | INV-010, INV-011 | Listado y detalle calculan y filtran la señal inclusiva de reorden por clínica; pruebas de límite pasan. |
| [ ] | **INV-T007 — Conjunto semilla seguro** | INV-012, INV-013 | Store carga datos deterministas con la cobertura exigida y cero PHI; prueba de auditoría de semilla pasa. |
| [ ] | **INV-T008 — Backoffice de inventario** | INV-001, INV-003, INV-004, INV-010, INV-011 | Vista responsive permite operar artículos, lotes y movimientos y hace visible el reorden por clínica; comprobación funcional y visual pasa. |
| [ ] | **INV-T009 — Documentación y matriz de trazabilidad** | INV-001 a INV-013 | README de ejecución y matriz `requisito → prueba → commit` reflejan el sistema verificado. |

## Regeneración por cambios de requisito

Ante un cambio, se editará primero `spec.md`; después se actualizará `plan.md` solo si cambia una decisión arquitectónica y se reemplazarán únicamente las filas afectadas de esta tabla. El PR deberá identificar las secciones modificadas y los IDs de tarea regenerados.