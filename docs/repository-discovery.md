# Reconocimiento del código base

## Resumen inicial y contraste con el repositorio

La primera hipótesis era que el monorepo ya podía contener una aplicación de backoffice lista para ampliar. La revisión del repositorio muestra que todavía es una plantilla: contiene carpetas, documentación y algunos tipos compartidos, pero no tiene una aplicación ejecutable ni un gestor de dependencias global configurado.

El contexto de negocio sí está disponible en `CONTEXT.md` y corresponde a HealthCore. El contexto describe la empresa, sus departamentos y sus problemas, pero no define todavía los valores concretos de tipos de incidencia, severidades, canales o estados.

## Convenciones confirmadas

1. **Separación por responsabilidad:** las interfaces van en `uis/`, las APIs y servicios en `services/`, los datos en `data/`, los componentes de IA en `agents/`, `skills/` y `mcps/`, y la documentación transversal en `docs/`.
2. **Aplicaciones organizadas por subcarpetas:** cada aplicación o servicio nuevo debe tener su propia subcarpeta y documentación local.
3. **Reutilización mediante paquetes:** los tipos, librerías y contratos compartidos deben vivir en `packages/`; existe el paquete `@repo/shared-types` en `packages/shared/`.
4. **Servicios centralizados:** el README recomienda una API centralizada con FastAPI dentro de `services/`, evitando crear microservicios demasiado pronto.
5. **Documentación previa:** antes de trabajar en una carpeta hay que leer su `README.md` y documentar lo que se añada.

## Gestión de dependencias y ejecución

El repositorio no tiene un `package.json` en la raíz, scripts globales ni un runner de workspace configurado. Por tanto, no existe actualmente un comando global para levantar todo el proyecto. Los nuevos componentes deberán documentar sus propias dependencias y comandos de ejecución.

## Mejora propuesta

Como propuesta para discutir con el equipo, se podría añadir en el futuro una guía de comandos de desarrollo y una estrategia común de ejecución para los componentes del monorepo. No se aplica ahora porque el repositorio todavía no tiene aplicaciones ejecutables y la convención actual no define un runner global.

## Fuentes revisadas

- `README.md`
- `CONTEXT.md`
- `docs/README.md`
- `uis/README.md`
- `services/README.md`
- `packages/README.md`
- `packages/shared/package.json`