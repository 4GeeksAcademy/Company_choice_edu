# Pila tecnológica

- Monorepo con responsabilidades separadas por carpetas.
- API: Python y FastAPI en `services/incident-api/`.
- Interfaz: HTML, CSS y JavaScript sin framework en `uis/backoffice/`.
- Contratos: TypeScript en `packages/shared/types/`.
- Pruebas de API: `unittest` y FastAPI `TestClient`.
- Almacenamiento actual: memoria del proceso; se pierde al reiniciar la API.
- No existe un gestor de dependencias global del monorepo.