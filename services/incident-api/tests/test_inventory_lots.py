import unittest
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.inventory_router import inventory_store
from app.main import app


class InventoryLotApiTest(unittest.TestCase):
    def setUp(self) -> None:
        inventory_store.clear()
        self.client = TestClient(app)
        item = self.client.post(
            "/inventory/items",
            json={
                "clinic_location": "Austin Central",
                "country": "us",
                "name": "Syringes",
                "category": "medical_consumables",
                "unit_of_measure": "box",
                "reorder_point": 5,
            },
        )
        self.item_id = item.json()["id"]
        self.payload = {
            "item_id": self.item_id,
            "lot_code": "LOT-001",
            "expiry_date": "2027-12-31",
            "received_at": datetime.now(timezone.utc).isoformat(),
        }

    def test_inv_003_creates_lists_and_rejects_duplicate_lot(self) -> None:
        created = self.client.post("/inventory/lots", json=self.payload)
        duplicate = self.client.post("/inventory/lots", json=self.payload)
        listing = self.client.get(f"/inventory/items/{self.item_id}/lots")

        self.assertEqual(created.status_code, 201)
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(len(listing.json()), 1)

    def test_inv_008_rejects_lot_for_missing_item(self) -> None:
        response = self.client.post(
            "/inventory/lots", json={**self.payload, "item_id": "missing"}
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()