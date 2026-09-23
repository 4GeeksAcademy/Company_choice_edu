# Incident API

API centralizada para registrar y gestionar incidencias operativas de HealthCore.

## Tecnología

- Python.
- FastAPI.
- Uvicorn para ejecutar el servidor local.

## Ejecución local

Desde esta carpeta:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://127.0.0.1:8000/docs`.

## Endpoints disponibles

- `GET /health`: comprueba que el servicio está disponible.
- `POST /incidents`: registra una incidencia.
- `GET /incidents/{incident_id}`: consulta una incidencia.
- `PATCH /incidents/{incident_id}/status`: cambia su estado y registra el actor y la fecha.
- `PATCH /incidents/{incident_id}/responsible-area`: cambia el área responsable y registra el actor y la fecha.
- `GET /incidents/{incident_id}/audit`: devuelve el historial de cambios.

Los datos se almacenan temporalmente en memoria y se pierden al reiniciar el servicio.

## Prueba funcional

Con el entorno virtual activado, desde esta carpeta:

```bash
python -c "from fastapi.testclient import TestClient; from app.main import app; client=TestClient(app); response=client.get('/health'); assert response.status_code == 200; print(response.json())"
```

## Estado

El servicio permite registrar y auditar cambios básicos de incidencias en memoria. La persistencia y la interfaz del backoffice se añadirán en pasos separados.