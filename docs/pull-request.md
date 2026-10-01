# Entrega: gestor centralizado de incidencias

## Resumen

Se añade un backoffice operativo para crear, editar, listar, filtrar, detallar y asignar incidencias de HealthCore. El sistema permite gestionar el ciclo de vida, consultar el volumen abierto por gravedad y revisar la trazabilidad de los cambios de estado y área responsable.

## Componentes

- Interfaz web estática en `uis/backoffice/`.
- API FastAPI en `services/incident-api/`.
- Contratos reutilizables en `packages/shared/types/`.
- Catálogos oficiales en `CONTEXT-company.md`.
- Reglas del agente en `.agents/rules/`.
- Contexto, stack, estado y plan en `memory-bank/`.

## Reglas aplicadas

- Se respetó la separación del monorepo entre interfaz, servicio, contratos y documentación.
- Los cambios de estado y área generan eventos inmutables con valor anterior, valor nuevo, autor y fecha UTC.
- Los valores de catálogo solo se implementaron después de registrarlos como decisión de producto.
- Cada fase relevante se validó y se confirmó mediante un commit independiente.
- El entorno virtual, archivos compilados y otros artefactos se excluyeron del control de versiones.

## Evidencias de prevención de desviaciones

- La regla de estructura evitó crear la aplicación directamente en la raíz: el backoffice vive en `uis/` y la API en `services/`.
- La regla de trazabilidad hizo que la asignación de área usara un endpoint auditado en lugar de sobrescribir el responsable sin historial.
- La regla de catálogos impidió añadir valores silenciosamente: la taxonomía se documentó y después se consolidó en `CONTEXT-company.md`.
- La regla de validación impidió confirmar `.venv/` y archivos `__pycache__/`; ambos están cubiertos por `.gitignore`.

## Discrepancias encontradas

- La hipótesis inicial suponía que ya existía una aplicación ampliable, pero el repositorio era una plantilla sin aplicaciones ejecutables.
- No había un gestor de paquetes ni un comando global del monorepo; cada componente mantiene su ejecución local documentada.
- `CONTEXT.md` describía el negocio, pero no contenía los catálogos exactos del gestor; estos se acordaron y registraron en `CONTEXT-company.md`.

## Mejora propuesta y no aplicada

Se propone definir en el futuro una estrategia común de ejecución y una guía de comandos para todo el monorepo. No se aplicó porque no existe todavía una convención de runner global y añadirla habría ampliado el alcance del práctico.

## Validación

- Prueba automatizada del flujo completo con `unittest` y `TestClient`.
- Comprobación de compilación de los módulos Python.
- Comprobación de formato con `git diff --check`.
- Validación manual del alta, dashboard, cambio de estado e historial desde el backoffice.

## Limitaciones del MVP

- Los datos se almacenan en memoria y se pierden al reiniciar la API.
- No se incluye autenticación ni autorización.
- El autor de cada cambio se recibe desde el cliente; una versión productiva debe obtenerlo de una identidad autenticada.
- El puerto público usado durante la demostración en Codespaces no es apropiado para datos sanitarios reales.
- Un despliegue productivo requiere controles adicionales de acceso, cifrado, retención y privacidad para HIPAA y UK GDPR.