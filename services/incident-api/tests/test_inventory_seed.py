import unittest
from datetime import date

from app.inventory_models import MovementType
from app.inventory_store import InventoryStore


class InventorySeedTest(unittest.TestCase):
    def test_inv_012_and_013_seed_has_required_coverage(self) -> None:
        store = InventoryStore()
        items = list(store._items.values())
        lots = list(store._lots.values())

        self.assertEqual(len(items), 15)
        self.assertGreaterEqual(len({item.clinic_location for item in items}), 4)
        self.assertEqual({item.country.value for item in items}, {"us", "uk"})
        self.assertEqual(len({item.category for item in items}), 4)
        self.assertGreaterEqual(len({lot.item_id for lot in lots}), 4)
        self.assertTrue(any(lot.expiry_date < date.today() for lot in lots))
        self.assertGreaterEqual(sum(store.item_view(item).below_reorder for item in items), 2)
        for item in items:
            self.assertEqual(
                {movement.movement_type for movement in store.list_movements(item.id)},
                set(MovementType),
            )


if __name__ == "__main__":
    unittest.main()