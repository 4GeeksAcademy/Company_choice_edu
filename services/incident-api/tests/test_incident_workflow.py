import unittest

from fastapi.testclient import TestClient

from app.main import app


class IncidentWorkflowTest(unittest.TestCase):
    def test_create_update_and_audit_incident(self) -> None:
        client = TestClient(app)
        payload = {
            "title": "EHR unavailable",
            "description": "The clinic cannot access the EHR",
            "type": "technology",
            "severity": "high",
            "channel": "phone",
        }

        created = client.post("/incidents", json=payload)

        self.assertEqual(created.status_code, 201)
        incident_id = created.json()["id"]

        listing = client.get("/incidents")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.json()), 1)
        filtered = client.get("/incidents", params={"severity": "high"})
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(len(filtered.json()), 1)
        summary = client.get("/incidents/summary/open-by-severity")
        self.assertEqual(summary.status_code, 200)
        self.assertEqual(summary.json()["high"], 1)

        status_update = client.patch(
            f"/incidents/{incident_id}/status",
            json={"status": "in-progress", "changed_by": "user-1"},
        )
        area_update = client.patch(
            f"/incidents/{incident_id}/responsible-area",
            json={"responsible_area": "technology", "changed_by": "user-2"},
        )
        audit = client.get(f"/incidents/{incident_id}/audit")

        self.assertEqual(status_update.status_code, 200)
        self.assertEqual(area_update.status_code, 200)
        self.assertEqual(audit.status_code, 200)
        self.assertEqual(len(audit.json()), 2)
        self.assertEqual(audit.json()[0]["changed_by"], "user-1")
        self.assertEqual(audit.json()[1]["changed_by"], "user-2")


if __name__ == "__main__":
    unittest.main()