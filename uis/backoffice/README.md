# HealthCore Backoffice

Interfaz web para gestionar incidencias e inventario operativo.

## Ejecución local

1. Desde la raíz, instala dependencias e inicia la API:

   ```bash
   npm install
   cd services/incident-api
   .venv/bin/uvicorn app.main:app --reload --port 8000
   ```

2. En otra terminal, desde la raíz, inicia el backoffice:

   ```bash
   npm run dev:backoffice
   ```

3. Abre `http://localhost:3001`.

La vista Next.js importa `getOpenIncidentSummary` desde `@repo/shared-types` y
muestra el resumen calculado por la API. Usa `INCIDENT_API_URL` para cambiar
`http://127.0.0.1:8000`.