"""test_details_crud.py
================================
CRUD integration tests for the **patient.details** model.

These tests exercise the full create‑read‑update‑delete life‑cycle as it would
run inside the Django ORM, including verification of the computed **age**
property and the model’s built‑in soft‑delete flag (`is_delete`).

Running
-------
```bash
python manage.py test patient.tests.test_details_crud -v 2
```
"""

from datetime import date
from django.test import TestCase
from patient.models import details


class DetailsCRUDTestCase(TestCase):
    """End‑to‑end CRUD checks for **details** instances."""

    def setUp(self):
        # Keep a baseline payload handy to minimise duplication in individual tests.
        self.valid_data = {
            "first_name": "John",
            "middle_name": "Q",
            "last_name": "Public",
            "gender": "Male",
            "BOD": date(1990, 1, 1),
            "contact_number": "09171234567",
            "email": "john.public@example.com",
        }

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def test_create_details_instance(self):
        """`details.objects.create()` should persist a new record and auto‑populate defaults."""
        initial = details.objects.count()

        person = details.objects.create(**self.valid_data)

        self.assertEqual(details.objects.count(), initial + 1)
        self.assertIsNotNone(person.pk)
        # default flags
        self.assertTrue(person.status)
        self.assertFalse(person.is_delete)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def test_retrieve_existing_instance(self):
        person = details.objects.create(**self.valid_data)

        fetched = details.objects.get(pk=person.pk)
        self.assertEqual(fetched.first_name, self.valid_data["first_name"])
        self.assertEqual(fetched.last_name, self.valid_data["last_name"])

        # Age property is an int > 0 and roughly correct (±1 year tolerance).
        expected_age = int((date.today() - self.valid_data["BOD"]).days / 365.25)
        self.assertEqual(fetched.age, expected_age)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def test_update_fields_and_save(self):
        person = details.objects.create(**self.valid_data)

        person.last_name = "Doe"
        person.save()

        refreshed = details.objects.get(pk=person.pk)
        self.assertEqual(refreshed.last_name, "Doe")

    # ------------------------------------------------------------------
    # Soft delete (toggle flag)
    # ------------------------------------------------------------------

    def test_soft_delete_flag(self):
        person = details.objects.create(**self.valid_data)
        person.is_delete = True
        person.save(update_fields=["is_delete"])  # only touch the flag

        refreshed = details.objects.get(pk=person.pk)
        self.assertTrue(refreshed.is_delete)

    # ------------------------------------------------------------------
    # Hard delete (row removal)
    # ------------------------------------------------------------------

    def test_hard_delete_removes_row(self):
        person = details.objects.create(**self.valid_data)
        pk = person.pk

        person.delete()

        self.assertFalse(details.objects.filter(pk=pk).exists())
