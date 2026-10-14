# Skill: validar entrega del Hito 4

## Objetivo

Verificar que una entrega de HealthCore está lista para abrir un Pull Request.

## Entradas

- Rama que se desea entregar.
- Aplicaciones o servicios modificados.
- Ruta de las capturas de website y backoffice.

## Criterios de aceptación

- [ ] La rama se llama `feature/agent-memory-bank`.
- [ ] `npm run typecheck` finaliza sin errores.
- [ ] `npm run build` finaliza sin errores.
- [ ] Las pruebas del servicio modificado pasan.
- [ ] `memory-bank/progress.md` refleja el estado actual.
- [ ] `git diff --check` no informa errores.
- [ ] Las capturas muestran `uis/website` y `uis/backoffice` renderizados.
- [ ] La PR apunta a `main` e incluye capturas y enlace a `AGENTS.md`.