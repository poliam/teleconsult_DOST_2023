"""
test_address_crud.py
====================
CRUD tests for the `address` model under the `patient` app.

Covers:
    - Create a new address instance
    - Retrieve and assert values
    - Update a field
    - Delete the instance

Run with:
    python manage.py test patient.tests.test_address_crud -v 2
"""

from django.test import TestCase
from patient.models import address, details


class AddressCRUDTest(TestCase):
    """Basic CRUD tests for the `address` model."""

    def setUp(self):
        # A related `details` record is required for the FK
        self.patient = details.objects.create(
            first_name="John",
            last_name="Doe",
            BOD="1990-01-01",
        )
        self.valid_data = {
            "details": self.patient,
            "current_street": "123 Main St",
            "current_city": "Manila",
            "current_country": "Philippines",
        }

    def test_create_address(self):
        addr = address.objects.create(**self.valid_data)
        self.assertIsNotNone(addr.pk)

    def test_read_address(self):
        addr = address.objects.create(**self.valid_data)
        fetched = address.objects.get(pk=addr.pk)
        self.assertEqual(fetched.current_city, "Manila")

    def test_update_address(self):
        addr = address.objects.create(**self.valid_data)
        addr.current_city = "Quezon City"
        addr.save()
        addr.refresh_from_db()
        self.assertEqual(addr.current_city, "Quezon City")

    def test_delete_address(self):
        addr = address.objects.create(**self.valid_data)
        pk = addr.pk
        addr.delete()
        self.assertFalse(address.objects.filter(pk=pk).exists())