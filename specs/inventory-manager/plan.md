# Plan arquitectónico del gestor de inventario

## Integración en el monorepo

El inventario se incorporará a la API FastAPI existente como un dominio aislado mediante `inventory_models.py`, `inventory_store.py` e `inventory_router.py`. Esto conserva un único punto de entrada para HealthCore sin mezclar las reglas de incidencias e inventario. El backoffice seguirá siendo HTML, CSS y JavaScript sin framework y tendrá una vista de inventario independiente que consume la misma API.

Los contratos reutilizables del frontend se añadirán a `packages/shared/types/index.ts`. La API continuará usando modelos Pydantic como contrato ejecutable y almacenamiento en memoria, de acuerdo con el alcance actual del monorepo.

## Modelo de datos

`InventoryItem`, `InventoryLot` e `InventoryMovement` serán entidades separadas e inmutables respecto de sus identificadores y fechas de creación. Los artículos guardarán su clínica y país; lotes y movimientos se relacionarán por identificador. No habrá entidad, columna ni operación de escritura para existencias.

Las cuatro clínicas semilla tendrán identificadores estables y país fijo. Los datos semilla se construirán con los catálogos oficiales y se cargarán al inicializar el store, lo que permite pruebas deterministas y una demostración reproducible.

## Cálculo de existencias y movimientos

`InventoryStore` será el dueño del cálculo de existencias y del registro atómico de movimientos. Cada lectura de artículo sumará los movimientos existentes: `inbound` aporta una cantidad positiva, `outbound` la resta y `adjustment` aporta su cantidad con signo. La respuesta administrativa compondrá el artículo persistido con `available_stock` y `below_reorder`, ambos de solo lectura.

Antes de anexar un movimiento, el store validará en memoria la existencia y relación de artículo/lote, la obligación de lote por categoría, la caducidad para salidas y el saldo resultante. Solo después de superar todas las validaciones se agregará el movimiento, evitando estados parciales. Los errores de dominio se traducirán en respuestas HTTP `404` para recursos inexistentes y `409` para conflictos con reglas del inventario.

La eliminación de un artículo se rechazará cuando tenga lotes o movimientos, porque borrarlos en cascada destruiría trazabilidad. Los ajustes usarán una cantidad distinta de cero con signo y un motivo obligatorio; las entradas y salidas usarán cantidades positivas.

## Protección de datos

Los modelos tendrán campos cerrados para impedir propiedades adicionales. Una validación común inspeccionará todos los textos libres de inventario y rechazará patrones evidentes de identificadores de paciente o PHI. Los mensajes de error y logs no reproducirán el contenido rechazado. Los datos semilla y pruebas usarán únicamente motivos operativos generales.

Esta validación reduce el riesgo en la frontera del sistema, pero no sustituye controles productivos de autorización, DLP y auditoría, que quedan fuera del MVP en memoria.

## API y backoffice

El router expondrá CRUD de artículos, creación y listado de lotes, creación y listado de movimientos, y lecturas de stock siempre derivado. El listado permitirá filtrar por clínica y por estado de reorden.

La vista administrativa mostrará métricas, filtros por clínica y categoría, una tabla con stock y umbral, una señal visible de reorden, detalle de lotes/movimientos y formularios para artículos, lotes y movimientos. Los formularios usarán exclusivamente los catálogos oficiales y adaptarán la obligatoriedad del lote a la categoría.

## Verificación

Las pruebas de API se organizarán por ID `INV-xxx` y comprobarán tanto respuestas como ausencia de mutación tras un rechazo. La semilla se verificará por cantidad, cobertura de países/categorías/lotes/movimientos, caducidad, reorden y ausencia de PHI. Una comprobación manual del backoffice cubrirá presentación y flujo en escritorio y móvil.