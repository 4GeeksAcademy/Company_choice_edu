import unittest

from pydantic import ValidationError

from app.inventory_models import InventoryItemCreate, InventoryMovementCreate


class InventoryModelTest(unittest.TestCase):
    def test_inv_001_rejects_unknown_catalog_values_and_fields(self) -> None:
        payload = {
            "clinic_location": "Austin Central",
            "country": "us",
            "name": "Nitrile gloves",
            "category": "ppe",
            "unit_of_measure": "box",
            "reorder_point": 12,
        }
        item = InventoryItemCreate(**payload)

        self.assertEqual(item.unit_of_measure.value, "box")
        with self.assertRaises(ValidationError):
            InventoryItemCreate(**{**payload, "category": "pharmaceuticals"})
        with self.assertRaises(ValidationError):
            InventoryItemCreate(**{**payload, "available_stock": 100})

    def test_inv_004_validates_movement_quantity_and_adjustment_reason(self) -> None:
        with self.assertRaises(ValidationError):
            InventoryMovementCreate(
                item_id="item-1", movement_type="outbound", quantity=-1
            )
        with self.assertRaises(ValidationError):
            InventoryMovementCreate(
                item_id="item-1", movement_type="adjustment", quantity=2
            )

        movement = InventoryMovementCreate(
            item_id="item-1",
            movement_type="adjustment",
            quantity=-2,
            reason="count_correction",
        )
        self.assertEqual(movement.quantity, -2)

    def test_inv_012_rejects_sensitive_text_without_echoing_it(self) -> None:
        sensitive_reason = "Used by patient MRN 849302"

        with self.assertRaises(ValidationError) as error:
            InventoryMovementCreate(
                item_id="item-1",
                movement_type="outbound",
                quantity=1,
                reason=sensitive_reason,
            )

        self.assertNotIn(sensitive_reason, str(error.exception))


if __name__ == "__main__":
    unittest.main()