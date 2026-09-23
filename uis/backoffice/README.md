# HealthCore Backoffice

Interfaz web para registrar y revisar incidencias operativas.

## Ejecución local

1. Inicia la API desde `services/incident-api`:

   ```bash
   .venv/bin/uvicorn app.main:app --reload --port 8000
   ```

2. En otra terminal, desde `uis/backoffice`, inicia el servidor estático:

   ```bash
   python -m http.server 4173
   ```

3. Abre `http://localhost:4173`.

La interfaz usa `http://localhost:8000` como URL de la API.