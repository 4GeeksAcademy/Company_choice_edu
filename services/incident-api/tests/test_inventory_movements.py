import unittest

from fastapi.testclient import TestClient

from app.inventory_router import inventory_store
from app.main import app


class InventoryMovementApiTest(unittest.TestCase):
    def setUp(self) -> None:
        inventory_store.clear()
        self.client = TestClient(app)
        item = self.client.post(
            "/inventory/items",
            json={
                "clinic_location": "Austin Central",
                "country": "us",
                "name": "Examination table",
                "category": "clinical_equipment",
                "unit_of_measure": "unit",
                "reorder_point": 2,
            },
        )
        self.item_id = item.json()["id"]

    def movement(self, movement_type: str, quantity: float, reason: str | None = None):
        return self.client.post(
            "/inventory/movements",
            json={
                "item_id": self.item_id,
                "movement_type": movement_type,
                "quantity": quantity,
                "reason": reason,
            },
        )

    def test_inv_004_and_005_records_movements_and_derives_stock(self) -> None:
        self.assertEqual(self.movement("inbound", 10).status_code, 201)
        self.assertEqual(self.movement("outbound", 3).status_code, 201)
        self.assertEqual(self.movement("adjustment", -1, "cycle count").status_code, 201)

        detail = self.client.get(f"/inventory/items/{self.item_id}")
        movements = self.client.get(f"/inventory/items/{self.item_id}/movements")

        self.assertEqual(detail.json()["available_stock"], 6)
        self.assertEqual(len(movements.json()), 3)


if __name__ == "__main__":
    unittest.main()