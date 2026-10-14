# Banco de memoria del proyecto

## Producto y negocio

HealthCore es una empresa sanitaria fundada en 2011. Opera 12 clínicas: 9 en Estados Unidos y 3 en el Reino Unido. Atiende consultas de atención primaria, especialistas, enfermedades crónicas y programas de prevención.

La empresa tiene aproximadamente 200 empleados y utiliza sistemas distintos para sus clínicas de Estados Unidos y Reino Unido. Esos sistemas no están integrados, por lo que la información operativa se encuentra repartida entre varias herramientas.

HealthCore debe cumplir con HIPAA en Estados Unidos y UK GDPR en el Reino Unido. La privacidad, la trazabilidad y el control de acceso son requisitos importantes para cualquier sistema nuevo.

## Problema que se va a resolver

El primer desarrollo del backoffice será un gestor centralizado de incidencias operativas. Las incidencias llegan por diferentes canales y actualmente pueden quedar dispersas entre correos, mensajes y registros separados.

El gestor deberá permitir registrar una incidencia, clasificarla, asignarla a un área responsable, consultar su estado y reconstruir los cambios de estado o responsable indicando quién los hizo y cuándo.

Los tipos, severidades, canales y áreas válidos deben tomarse del contexto oficial del proyecto y no inventarse durante la implementación.

## Estructura y stack conocido

El repositorio es un monorepo organizado por responsabilidades:

- `uis/`: interfaces de usuario, incluido el futuro backoffice.
- `services/`: APIs y servicios de backend.
- `packages/`: paquetes reutilizables y tipos compartidos.
- `data/`: datos, pipelines y conjuntos de evaluación.
- `agents/`, `skills/` y `mcps/`: componentes relacionados con IA.
- `docs/`: documentación transversal.
- `infra/`, `scripts/` e `internal/`: infraestructura y herramientas internas.

Actualmente existe un paquete de tipos compartidos en `packages/shared/`. El README del repositorio recomienda una API centralizada con FastAPI para los servicios, pero todavía no hay una aplicación ejecutable ni un runner global configurado.

## Estado actual

- La rama de trabajo es `feature/incident-manager`.
- El repositorio parte de una plantilla con estructura y documentación base.
- `CONTEXT.md` contiene el contexto oficial de HealthCore.
- No hay todavía un gestor de incidencias implementado.
- No hay todavía una interfaz, API, base de datos ni historial de auditoría para este gestor.
- El siguiente entregable después de esta memoria será definir las reglas del proyecto y del negocio antes de implementar funcionalidad.

## Fuentes consultadas

- `CONTEXT.md`
- `README.md`
- `docs/README.md`