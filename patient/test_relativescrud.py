from django.test import TestCase
from patient.models import details,relatives


class RelativesCRUDTest(TestCase):
    """Basic CRUD tests for the `relatives` model."""

    def setUp(self):
        self.patient = details.objects.create(
            first_name="John",
            last_name="Doe",
            BOD="1990-01-01",
        )
        self.valid_data = {
            "details": self.patient,
            "first_name": "Anna",
            "last_name": "Doe",
            "relationship": "Sister",
            "DOB": "2000-07-10",
        }

    def test_create_relative(self):
        rel = relatives.objects.create(**self.valid_data)
        self.assertIsNotNone(rel.pk)

    def test_read_relative(self):
        rel = relatives.objects.create(**self.valid_data)
        fetched = relatives.objects.get(pk=rel.pk)
        self.assertEqual(fetched.first_name, "Anna")

    def test_update_relative(self):
        rel = relatives.objects.create(**self.valid_data)
        rel.relationship = "Brother"
        rel.save()
        rel.refresh_from_db()
        self.assertEqual(rel.relationship, "Brother")

    def test_delete_relative(self):
        rel = relatives.objects.create(**self.valid_data)
        pk = rel.pk
        rel.delete()
        self.assertFalse(relatives.objects.filter(pk=pk).exists())
