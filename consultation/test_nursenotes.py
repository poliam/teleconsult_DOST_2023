from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from consultation.models import nurse_notes, encounter, details

User = get_user_model()


class NurseNotesCRUDTest(TestCase):
    """Basic CRUD tests for the `nurse_notes` model."""

    def setUp(self):
        # Create a user who will author the nurse note
        self.user = User.objects.create_user(username="nurse", password="password")

        # Minimal patient details record to satisfy FK constraints
        self.patient_details = details.objects.create(first_name="Jane", last_name="Doe")

        # Create a basic encounter record linked to the patient & nurse
        self.encounter = encounter.objects.create(
            details=self.patient_details,
            consulted_by=self.user,
            consultation_date=timezone.now().date(),
        )

    def test_create_nurse_note(self):
        """Ensure we can create a nurse note and its fields persist."""
        note = nurse_notes.objects.create(
            encounter=self.encounter,
            comment="Initial assessment",
            create_by=self.user,
        )
        self.assertIsNotNone(note.id)
        self.assertEqual(note.comment, "Initial assessment")
        self.assertFalse(note.is_delete)

    def test_read_nurse_note(self):
        """Ensure we can read back a saved nurse note."""
        note = nurse_notes.objects.create(
            encounter=self.encounter,
            comment="Vitals taken",
            create_by=self.user,
        )
        fetched = nurse_notes.objects.get(pk=note.pk)
        self.assertEqual(fetched.comment, "Vitals taken")
        self.assertEqual(fetched.encounter, self.encounter)

    # def test_update_nurse_note(self):
    #     """Ensure we can update a nurse note's comment."""
    #     note = nurse_notes.objects.create(
    #         encounter=self.encounter,
    #         comment="Old comment",
    #         create_by=self.user,
    #     )
    #     note.comment = "Updated comment"
    #     note.save()
    #     updated = nurse_notes.objects.get(pk=note.pk)
    #     self.assertEqual(updated.comment, "Updated comment")

    # def test_delete_nurse_note(self):
    #     """Ensure deleting a nurse note removes it from the database."""
    #     note = nurse_notes.objects.create(
    #         encounter=self.encounter,
    #         comment="To be deleted",
    #         create_by=self.user,
    #     )
    #     note_id = note.pk
    #     note.delete()
    #     self.assertFalse(nurse_notes.objects.filter(pk=note_id).exists())
