from django.test import TestCase
from consultation.models import history_present_illness, encounter
from datetime import datetime

class HistoryPresentIllnessCRUDTest(TestCase):
    def setUp(self):
        self.encounter = encounter.objects.create(
            consultation_date=datetime(2024, 1, 1)
        )

    def test_create_history_present_illness(self):
        hpi = history_present_illness.objects.create(
            encounter=self.encounter,
            number="123",
            calendrical="2025-07-17",
            details="Patient details here."
        )
        self.assertIsNotNone(hpi.id)
        self.assertEqual(hpi.encounter, self.encounter)
        self.assertEqual(hpi.number, "123")
        self.assertEqual(hpi.details, "Patient details here.")

    def test_read_history_present_illness(self):
        hpi = history_present_illness.objects.create(
            encounter=self.encounter,
            number="456",
            calendrical="2025-07-17",
            details="Read test."
        )
        fetched = history_present_illness.objects.get(pk=hpi.id)
        self.assertEqual(fetched.details, "Read test.")

    # def test_update_history_present_illness(self):
    #     hpi = history_present_illness.objects.create(
    #         encounter=self.encounter,
    #         number="789",
    #         calendrical="2025-07-17",
    #         details="Update test."
    #     )
    #     hpi.details = "Updated details."
    #     hpi.save()
    #     updated = history_present_illness.objects.get(pk=hpi.id)
    #     self.assertEqual(updated.details, "Updated details.")

    def test_delete_history_present_illness(self):
        hpi = history_present_illness.objects.create(
            encounter=self.encounter,
            number="000",
            calendrical="2025-07-17",
            details="Delete test."
        )
        hpi_id = hpi.id
        hpi.delete()
        with self.assertRaises(history_present_illness.DoesNotExist):
            history_present_illness.objects.get(pk=hpi_id)

#python manage.py test consultation.test_crud_history_present_illness