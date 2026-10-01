from fastapi import APIRouter, HTTPException, Response, status

from .inventory_models import (
    InventoryItem,
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemView,
    InventoryLot,
    InventoryLotCreate,
    InventoryMovement,
    InventoryMovementCreate,
)
from .inventory_store import InventoryConflictError, InventoryStore


router = APIRouter(prefix="/inventory", tags=["inventory"])
inventory_store = InventoryStore()


@router.post("/items", response_model=InventoryItem, status_code=status.HTTP_201_CREATED)
def create_item(payload: InventoryItemCreate) -> InventoryItem:
    return inventory_store.create_item(payload)


@router.get("/items", response_model=list[InventoryItemView])
def list_items(clinic_location: str | None = None) -> list[InventoryItemView]:
    return [inventory_store.item_view(item) for item in inventory_store.list_items(clinic_location)]


@router.get("/items/{item_id}", response_model=InventoryItemView)
def get_item(item_id: str) -> InventoryItemView:
    item = inventory_store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory_store.item_view(item)


@router.patch("/items/{item_id}", response_model=InventoryItem)
def update_item(item_id: str, payload: InventoryItemUpdate) -> InventoryItem:
    item = inventory_store.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str) -> Response:
    try:
        deleted = inventory_store.delete_item(item_id)
    except InventoryConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    if not deleted:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/lots", response_model=InventoryLot, status_code=status.HTTP_201_CREATED)
def create_lot(payload: InventoryLotCreate) -> InventoryLot:
    try:
        return inventory_store.create_lot(payload)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error.args[0])) from error
    except InventoryConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.get("/items/{item_id}/lots", response_model=list[InventoryLot])
def list_lots(item_id: str) -> list[InventoryLot]:
    try:
        return inventory_store.list_lots(item_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error.args[0])) from error


@router.post(
    "/movements",
    response_model=InventoryMovement,
    status_code=status.HTTP_201_CREATED,
)
def create_movement(payload: InventoryMovementCreate) -> InventoryMovement:
    return inventory_store.create_movement(payload)


@router.get("/items/{item_id}/movements", response_model=list[InventoryMovement])
def list_movements(item_id: str) -> list[InventoryMovement]:
    return inventory_store.list_movements(item_id)

