from django.test import TestCase
from django.contrib.auth.models import User
from consultation.models import encounter
from patient.models import details
from django.core.exceptions import ValidationError

class AppointmentFormValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.patient = details.objects.create(first_name='Jane', last_name='Smith')

    def test_valid_form(self):
        appointment = encounter(
            details=self.patient,
            reason_for_interaction='Follow-up',
            consultation_date='2025-07-14',
            consulted_by=self.user
        )
        # Should not raise
        try:
            appointment.full_clean()
        except Exception:
            self.fail('Valid appointment data should not raise ValidationError')

    def test_default_reason_for_interaction(self):
        appointment = encounter(
            details=self.patient,
            consultation_date='2025-07-14',
            consulted_by=self.user
        )
        appointment.full_clean()
        self.assertEqual(appointment.reason_for_interaction, "Outpatient")

    def test_invalid_date_format(self):
        appointment = encounter(
            details=self.patient,
            reason_for_interaction='Checkup',
            consultation_date='invalid-date',
            consulted_by=self.user
        )
        with self.assertRaises(ValidationError):
            appointment.full_clean()


# python manage.py test appointments.test_form_validation