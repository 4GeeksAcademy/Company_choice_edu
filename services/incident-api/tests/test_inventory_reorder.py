import unittest

from fastapi.testclient import TestClient

from app.inventory_router import inventory_store
from app.main import app


class InventoryReorderTest(unittest.TestCase):
    def setUp(self) -> None:
        inventory_store.clear()
        self.client = TestClient(app)

    def create_item(self, clinic: str, reorder_point: float) -> str:
        response = self.client.post("/inventory/items", json={
            "clinic_location": clinic, "country": "us", "name": f"Masks {clinic}",
            "category": "ppe", "unit_of_measure": "box", "reorder_point": reorder_point,
        })
        return response.json()["id"]

    def test_inv_010_and_011_reorder_is_inclusive_and_scoped_by_clinic(self) -> None:
        item_id = self.create_item("Austin Central", 5)
        self.create_item("Boston North", 5)
        self.client.post("/inventory/movements", json={
            "item_id": item_id, "movement_type": "inbound", "quantity": 5,
        })

        detail = self.client.get(f"/inventory/items/{item_id}")
        listing = self.client.get("/inventory/items", params={
            "clinic_location": "Austin Central", "below_reorder": True,
        })

        self.assertTrue(detail.json()["below_reorder"])
        self.assertEqual([item["id"] for item in listing.json()], [item_id])


if __name__ == "__main__":
    unittest.main()