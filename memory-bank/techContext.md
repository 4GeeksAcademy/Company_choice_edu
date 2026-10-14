# Contexto técnico

- Monorepo npm con Node.js 22, Next.js, React y TypeScript.
- Sitio público: `uis/website`, puerto 3000.
- Aplicación interna: `uis/backoffice`, puerto 3001.
- API FastAPI: `services/incident-api`, puerto 8000.
- Contratos y cliente HTTP compartidos: `packages/shared`; el backoffice importa `getOpenIncidentSummary` desde `@repo/shared-types`.
- Persistencia en memoria y ausencia de autenticación: límites aceptados del MVP, no aptos para producción sanitaria.

Las aplicaciones se validan desde la raíz con `npm run typecheck` y `npm run build`. Las pruebas Python se ejecutan desde `services/incident-api` con `.venv/bin/python -m unittest discover -s tests`.