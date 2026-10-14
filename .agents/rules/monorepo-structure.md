# Regla: estructura del monorepo

- Modo: siempre.
- Alcance: todos los archivos del repositorio.

## Reglas

- Las interfaces se colocan bajo `uis/`.
- Las APIs y servicios se colocan bajo `services/`.
- Los tipos compartidos se colocan bajo `packages/`.
- La documentación transversal se coloca bajo `docs/` o `memory-bank/`.
- No se crean aplicaciones nuevas directamente en la raíz.
- Antes de añadir archivos en una carpeta se lee su `README.md`.