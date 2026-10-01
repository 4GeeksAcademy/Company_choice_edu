# Reglas de trabajo del proyecto

## Inicio de sesión obligatorio

Antes de editar, leer en este orden:

1. `memory-bank/projectbrief.md`
2. `memory-bank/techContext.md`
3. `memory-bank/progress.md`
4. `CONTEXT-company.md` y el archivo `CONTEXT*.md` relacionado con la tarea

## Organización del monorepo

- Las interfaces de usuario se colocan en `uis/`.
- Las APIs y servicios de backend se colocan en `services/`.
- Los tipos y librerías reutilizables se colocan en `packages/`.
- La documentación transversal se coloca en `docs/`.
- Los scripts operativos se colocan en `scripts/`.
- No se deben colocar aplicaciones nuevas directamente en la raíz del repositorio.

## Implementación

- Leer `README.md` de la carpeta correspondiente antes de añadir archivos allí.
- Respetar las tecnologías y convenciones que ya existan en el repositorio.
- No añadir dependencias ni un gestor de paquetes global sin una necesidad justificada.
- Reutilizar los tipos compartidos cuando una interfaz y un servicio necesiten el mismo contrato.
- Mantener separadas la interfaz, la API, los datos y la documentación.

## Incidencias

- Los tipos, severidades, canales y estados deben proceder del contexto oficial o de una decisión documentada.
- No inventar valores de negocio cuando falte información en el contexto.
- Toda incidencia debe tener trazabilidad de los cambios de estado y responsable.
- Cada registro de auditoría debe conservar quién hizo el cambio y cuándo.
- Las funcionalidades que manejen datos sanitarios deben considerar HIPAA y UK GDPR.

## Documentación y cambios

- Documentar cada componente nuevo con un README cuando corresponda.
- Crear commits pequeños y separados por etapa relevante.
- Usar mensajes de commit descriptivos.
- Trabajar en la rama `feature/agent-memory-bank` para este hito.

## Flujo previo a cada commit

1. Ejecutar `npm run typecheck` desde la raíz para cambios TypeScript.
2. Ejecutar `npm run build` y las pruebas específicas del servicio afectado.
3. Actualizar `memory-bank/progress.md` cuando cambie el comportamiento o el estado del proyecto.
4. Ejecutar `git diff --check` y revisar `git diff --stat` para confirmar el alcance.
5. Confirmar que no se incluyen secretos, PHI ni artefactos generados.

## Áreas protegidas

No modificar sin confirmación humana explícita:

- `.github/workflows/` y cualquier configuración de CI/CD.
- `package-lock.json` u otros lockfiles generados, salvo actualización de dependencias aprobada.
- Migraciones, credenciales y configuración de despliegue bajo `infra/`.
- Una aplicación distinta de la indicada en la tarea.
- Contratos públicos de `services/` o `packages/` que rompan consumidores existentes.