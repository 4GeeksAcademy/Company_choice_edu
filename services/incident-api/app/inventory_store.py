from datetime import date, datetime, timezone
from uuid import uuid4

from .inventory_models import (
    InventoryItem,
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemView,
    InventoryLot,
    InventoryLotCreate,
    InventoryMovement,
    InventoryMovementCreate,
    LOT_CONTROLLED_CATEGORIES,
    MovementType,
)


class InventoryConflictError(Exception):
    pass


class InventoryStore:
    def __init__(self) -> None:
        self._items: dict[str, InventoryItem] = {}
        self._lots: dict[str, InventoryLot] = {}
        self._movements: list[InventoryMovement] = []

    def clear(self) -> None:
        self._items.clear()
        self._lots.clear()
        self._movements.clear()

    def create_item(self, payload: InventoryItemCreate) -> InventoryItem:
        now = datetime.now(timezone.utc)
        item = InventoryItem(
            id=str(uuid4()),
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )
        self._items[item.id] = item
        return item

    def get_item(self, item_id: str) -> InventoryItem | None:
        return self._items.get(item_id)

    def list_items(self, clinic_location: str | None = None) -> list[InventoryItem]:
        return [
            item
            for item in self._items.values()
            if clinic_location is None or item.clinic_location == clinic_location
        ]

    def update_item(
        self, item_id: str, payload: InventoryItemUpdate
    ) -> InventoryItem | None:
        item = self.get_item(item_id)
        if item is None:
            return None
        updates = payload.model_dump(exclude_none=True)
        updated = item.model_copy(
            update={**updates, "updated_at": datetime.now(timezone.utc)}
        )
        self._items[item_id] = updated
        return updated

    def delete_item(self, item_id: str) -> bool:
        if item_id not in self._items:
            return False
        has_lots = any(getattr(lot, "item_id", None) == item_id for lot in self._lots.values())
        has_movements = any(
            getattr(movement, "item_id", None) == item_id
            for movement in self._movements
        )
        if has_lots or has_movements:
            raise InventoryConflictError("Item history must be preserved")
        del self._items[item_id]
        return True

    def create_lot(self, payload: InventoryLotCreate) -> InventoryLot:
        if payload.item_id not in self._items:
            raise KeyError("Inventory item not found")
        if any(
            lot.item_id == payload.item_id and lot.lot_code == payload.lot_code
            for lot in self._lots.values()
        ):
            raise InventoryConflictError("Lot code already exists for item")
        lot = InventoryLot(id=str(uuid4()), **payload.model_dump())
        self._lots[lot.id] = lot
        return lot

    def list_lots(self, item_id: str) -> list[InventoryLot]:
        if item_id not in self._items:
            raise KeyError("Inventory item not found")
        return [lot for lot in self._lots.values() if lot.item_id == item_id]

    def create_movement(self, payload: InventoryMovementCreate) -> InventoryMovement:
        item = self.get_item(payload.item_id)
        if item is None:
            raise KeyError("Inventory item not found")
        lot = self._lots.get(payload.lot_id) if payload.lot_id else None
        if payload.lot_id and lot is None:
            raise KeyError("Inventory lot not found")
        if lot and lot.item_id != payload.item_id:
            raise InventoryConflictError("Lot does not belong to item")
        if item.category in LOT_CONTROLLED_CATEGORIES and lot is None:
            raise InventoryConflictError("Lot is required for this item")
        if (
            payload.movement_type == MovementType.outbound
            and lot
            and lot.expiry_date < date.today()
        ):
            raise InventoryConflictError("Expired lot cannot be used for outbound movement")
        delta = -payload.quantity if payload.movement_type == MovementType.outbound else payload.quantity
        if self.available_stock(payload.item_id) + delta < 0:
            raise InventoryConflictError("Movement would leave stock negative")
        movement = InventoryMovement(
            id=str(uuid4()),
            created_at=datetime.now(timezone.utc),
            **payload.model_dump(),
        )
        self._movements.append(movement)
        return movement

    def list_movements(self, item_id: str) -> list[InventoryMovement]:
        return [movement for movement in self._movements if movement.item_id == item_id]

    def available_stock(self, item_id: str) -> float:
        stock = 0.0
        for movement in self.list_movements(item_id):
            if movement.movement_type == MovementType.inbound:
                stock += movement.quantity
            elif movement.movement_type == MovementType.outbound:
                stock -= movement.quantity
            else:
                stock += movement.quantity
        return stock

    def item_view(self, item: InventoryItem) -> InventoryItemView:
        stock = self.available_stock(item.id)
        return InventoryItemView(
            **item.model_dump(),
            available_stock=stock,
            below_reorder=stock <= item.reorder_point,
        )
