from datetime import datetime, timezone
from uuid import uuid4

from .inventory_models import InventoryItem, InventoryItemCreate, InventoryItemUpdate


class InventoryConflictError(Exception):
    pass


class InventoryStore:
    def __init__(self) -> None:
        self._items: dict[str, InventoryItem] = {}
        self._lots: dict[str, object] = {}
        self._movements: list[object] = []

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
