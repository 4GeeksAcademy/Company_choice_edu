# Especificación del gestor de inventario

## Alcance y catálogos

El gestor mantiene suministros por clínica para HealthCore. Las unidades admitidas son `unit`, `box`, `ml` y `tablet`; las categorías admitidas son `ppe`, `medical_consumables`, `otc_medication` y `clinical_equipment`; los países admitidos son `us` y `uk`; y los tipos de movimiento admitidos son `inbound`, `outbound` y `adjustment`.

Un artículo contiene `clinic_location`, `country`, `name`, `category`, `unit_of_measure`, `reorder_point`, `created_at` y `updated_at`. Un lote contiene `item_id`, `lot_code`, `expiry_date` y `received_at`. Un movimiento contiene `item_id`, `lot_id` nulable, `movement_type`, `quantity`, `reason` y `created_at`.

## Criterios de aceptación

- **INV-001 (Ubiquitous):** El sistema deberá permitir crear, consultar, listar, actualizar y eliminar artículos únicamente con los campos y valores de catálogo definidos en esta especificación.
- **INV-002 (State-driven):** Mientras un artículo pertenezca a `medical_consumables` u `otc_medication`, el sistema deberá exigir un lote válido en cada movimiento; para las demás categorías el lote será opcional.
- **INV-003 (Ubiquitous):** El sistema deberá permitir registrar lotes con un código único por artículo, fecha de caducidad y fecha de recepción, y deberá permitir consultarlos por artículo.
- **INV-004 (Event-driven):** Cuando se registre un movimiento, el sistema deberá conservar su tipo, una cantidad positiva, su motivo operativo y una marca de tiempo; el motivo será obligatorio para movimientos `adjustment`.
- **INV-005 (Ubiquitous):** El sistema deberá calcular las existencias disponibles de cada artículo exclusivamente a partir de la suma de sus movimientos: las entradas incrementan, las salidas reducen y los ajustes aplican una variación con signo. Las existencias nunca deberán almacenarse ni exponerse como un campo editable.
- **INV-006 (Unwanted):** Si un movimiento dejara las existencias disponibles por debajo de cero, el sistema deberá rechazarlo sin registrar el movimiento ni alterar las existencias calculadas.
- **INV-007 (Unwanted):** Si un movimiento referencia un artículo inexistente, el sistema deberá rechazarlo sin registrar ningún cambio.
- **INV-008 (Unwanted):** Si un movimiento referencia un lote inexistente o un lote que no pertenece al artículo indicado, el sistema deberá rechazarlo sin registrar ningún cambio.
- **INV-009 (Unwanted):** Si una salida referencia un lote cuya `expiry_date` ya pasó, el sistema deberá rechazarla sin registrar ningún cambio.
- **INV-010 (Event-driven):** Cuando las existencias disponibles de un artículo sean menores o iguales a su `reorder_point`, el sistema deberá marcarlo como bajo punto de reorden tanto en el listado como en el detalle administrativo de su clínica.
- **INV-011 (Ubiquitous):** El sistema deberá controlar artículos, lotes, movimientos, existencias y puntos de reorden de forma independiente por clínica, sin agregar movimientos entre ubicaciones.
- **INV-012 (Ubiquitous):** El sistema no deberá aceptar, almacenar, registrar ni devolver PHI, identificadores de pacientes ni datos regulados por HIPAA o UK GDPR en campos de inventario, motivos, logs, eventos, documentos o respuestas.
- **INV-013 (Event-driven):** Cuando se solicite el conjunto inicial, el sistema deberá ofrecer al menos 15 artículos distribuidos entre al menos cuatro clínicas de `us` y `uk`, cubrir las cuatro categorías, incluir al menos cuatro artículos con lote y un lote caducado, marcar al menos dos artículos bajo reorden y proporcionar para cada artículo movimientos `inbound`, `outbound` y `adjustment`.

## Invariantes de contrato

- Las cantidades de `inbound` y `outbound` son positivas. La cantidad de `adjustment` es distinta de cero y su signo expresa el incremento o la reducción.
- `reorder_point` es numérico, no negativo y se define para cada artículo en una clínica.
- Un lote pertenece a un único artículo y no puede utilizarse para mover otro artículo.
- El motivo describe una causa operativa, nunca un paciente ni su atención identificable.
- Eliminar un artículo con movimientos o lotes registrados no puede borrar su trazabilidad histórica.