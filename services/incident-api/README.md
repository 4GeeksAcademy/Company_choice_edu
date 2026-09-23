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

## Estado

El servicio comienza con un endpoint de salud. Los endpoints de incidencias y la persistencia se añadirán en pasos separados.