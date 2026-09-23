# Reglas de trabajo del proyecto

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
- Validar los cambios antes de confirmarlos.
- Crear commits pequeños y separados por etapa relevante.
- Usar mensajes de commit descriptivos.
- Trabajar en la rama `feature/incident-manager` para este desarrollo.