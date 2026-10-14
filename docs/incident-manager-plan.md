# Plan del gestor de incidencias

## Objetivo

Construir un gestor interno para que Operaciones registre, clasifique, asigne y consulte incidencias de HealthCore desde un único backoffice.

## Ubicación prevista

- Interfaz: `uis/backoffice/`.
- API: `services/incident-api/`.
- Contratos y tipos compartidos: `packages/shared/`.
- Documentación y decisiones: `docs/`.

## Alcance inicial

1. Crear una incidencia con su información básica.
2. Clasificarla usando los valores oficiales del contexto.
3. Asignarla a un área responsable.
4. Consultar y cambiar su estado.
5. Consultar el historial de cambios.
6. Registrar en cada cambio el actor y la fecha.

## Orden de implementación

1. Confirmar tipos, severidades, canales y estados.
2. Definir los tipos compartidos de la incidencia y del evento de auditoría.
3. Implementar la API y sus validaciones.
4. Implementar la interfaz del backoffice.
5. Añadir pruebas para el registro y la trazabilidad.
6. Verificar el checklist y documentar cómo ejecutar cada componente.

## Decisiones pendientes

No se implementarán formularios ni validaciones para tipos, severidades, canales o estados hasta confirmar sus valores en el contexto oficial del gestor.