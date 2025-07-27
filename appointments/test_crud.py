from django.test import TestCase
from django.contrib.auth.models import User
from consultation.models import encounter
from patient.models import details

class AppointmentCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.patient = details.objects.create(first_name='John', last_name='Doe')
        self.encounter_data = {
            'details': self.patient,
            'reason_for_interaction': 'Routine checkup',
            'encounter_notes': 'Patient is healthy',
            'treatment_recommendations': 'Continue healthy lifestyle',
            'consultation_date': '2025-07-14',
            'consulted_by': self.user,
        }

    def test_create_appointment(self):
        appointment = encounter.objects.create(**self.encounter_data)
        self.assertIsNotNone(appointment.id)
        self.assertEqual(appointment.reason_for_interaction, 'Routine checkup')

    def test_read_appointment(self):
        appointment = encounter.objects.create(**self.encounter_data)
        fetched = encounter.objects.get(id=appointment.id)
        self.assertEqual(fetched.encounter_notes, 'Patient is healthy')

    def test_update_appointment(self):
        appointment = encounter.objects.create(**self.encounter_data)
        appointment.encounter_notes = 'Updated notes'
        appointment.save()
        updated = encounter.objects.get(id=appointment.id)
        self.assertEqual(updated.encounter_notes, 'Updated notes')

    def test_delete_appointment(self):
        appointment = encounter.objects.create(**self.encounter_data)
        appointment.delete()
        with self.assertRaises(encounter.DoesNotExist):
            encounter.objects.get(id=appointment.id)

            
# python manage.py test appointments.test_crud