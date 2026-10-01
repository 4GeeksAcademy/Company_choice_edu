# Regla: validación y commits

- Modo: solicitado por el agente antes de cada commit.
- Alcance: todos los cambios de código y documentación.

## Reglas

- Se ejecuta la validación más cercana al cambio antes de confirmar.
- Cada fase relevante del checklist usa un commit independiente.
- El mensaje del commit describe la fase y no agrupa cambios no relacionados.
- No se confirma un archivo generado, una credencial ni un entorno virtual.
- Las nuevas dependencias deben estar declaradas y justificadas en la documentación o en una regla.