import unittest
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.inventory_router import inventory_store
from app.main import app


class InventoryMovementRejectionTest(unittest.TestCase):
    def setUp(self) -> None:
        inventory_store.clear()
        self.client = TestClient(app)
        self.item_id = self.create_item("ppe", "Gloves")
        self.controlled_id = self.create_item("medical_consumables", "Syringes")
        self.lot_id = self.create_lot(self.controlled_id, "2027-12-31")

    def create_item(self, category: str, name: str) -> str:
        response = self.client.post("/inventory/items", json={
            "clinic_location": "Austin Central", "country": "us", "name": name,
            "category": category, "unit_of_measure": "box", "reorder_point": 2,
        })
        return response.json()["id"]

    def create_lot(self, item_id: str, expiry: str) -> str:
        response = self.client.post("/inventory/lots", json={
            "item_id": item_id, "lot_code": f"LOT-{expiry}", "expiry_date": expiry,
            "received_at": datetime.now(timezone.utc).isoformat(),
        })
        return response.json()["id"]

    def post(self, item_id: str, movement_type: str, quantity: float, lot_id=None):
        return self.client.post("/inventory/movements", json={
            "item_id": item_id, "lot_id": lot_id,
            "movement_type": movement_type, "quantity": quantity,
        })

    def test_inv_006_and_007_reject_negative_stock_and_missing_item_atomically(self) -> None:
        self.assertEqual(self.post(self.item_id, "outbound", 1).status_code, 409)
        self.assertEqual(self.post("missing", "inbound", 1).status_code, 404)
        self.assertEqual(len(inventory_store._movements), 0)

    def test_inv_002_and_008_require_matching_existing_lot(self) -> None:
        other_id = self.create_item("medical_consumables", "Gauze")
        self.assertEqual(self.post(self.controlled_id, "inbound", 2).status_code, 409)
        self.assertEqual(self.post(self.controlled_id, "inbound", 2, "missing").status_code, 404)
        self.assertEqual(self.post(other_id, "inbound", 2, self.lot_id).status_code, 409)
        self.assertEqual(len(inventory_store._movements), 0)

    def test_inv_009_rejects_expired_lot_for_outbound(self) -> None:
        expired_id = self.create_lot(self.controlled_id, "2020-01-01")
        self.assertEqual(self.post(self.controlled_id, "inbound", 3, expired_id).status_code, 201)
        self.assertEqual(self.post(self.controlled_id, "outbound", 1, expired_id).status_code, 409)
        self.assertEqual(len(inventory_store._movements), 1)


if __name__ == "__main__":
    unittest.main()