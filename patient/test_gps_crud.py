from django.test import TransactionTestCase, override_settings
from django.contrib.auth.models import User
from patient.models import details, global_psychotrauma_screen, considering_event
from datetime import datetime, timedelta
from patient.test_settings import DATABASES

@override_settings(DATABASES=DATABASES)
class GlobalPsychotraumaScreenCRUDTests(TransactionTestCase):
    """
    Test cases for Global Psychotrauma Screen CRUD operations
    Using TransactionTestCase to handle database transactions better
    """
    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test patient
        self.patient = details.objects.create(
            first_name='John',
            last_name='Doe',
            BOD=datetime.now().date() - timedelta(days=365*30),  # 30 years old
            gender='Male'
        )
        
        # Create a basic GPS record
        self.gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='Test trauma event',
            event_happened='last week',
            physical_violence='to yourself',
            sexual_violence='happened to someone else',
            emotional_abuse='to yourself',
            serious_injury='happened to someone else',
            life_threatening='to yourself',
            sudden_death_of_loved_one=True,
            cause_harm_to_others=False,
            covid=False,
            single_event_occurring='Yes'
        )
        
        # Create associated considering events
        self.considering_event1 = considering_event.objects.create(
            global_psychotrauma_screen=self.gps,
            considering_event_1='Yes',
            considering_event_2='No'
        )

    def test_gps_creation(self):
        """Test creating a new GPS record"""
        new_gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='New trauma event',
            event_happened='last month'
        )
        self.assertIsInstance(new_gps, global_psychotrauma_screen)
        self.assertEqual(new_gps.event_description, 'New trauma event')
        self.assertEqual(new_gps.details, self.patient)

    def test_gps_read(self):
        """Test reading GPS records"""
        # Test retrieving single record
        retrieved_gps = global_psychotrauma_screen.objects.get(pk=self.gps.pk)
        self.assertEqual(retrieved_gps.event_description, 'Test trauma event')
        self.assertTrue(retrieved_gps.sudden_death_of_loved_one)
        
        # Test retrieving all records for a patient
        patient_gps_records = global_psychotrauma_screen.objects.filter(
            details=self.patient
        )
        self.assertEqual(patient_gps_records.count(), 1)

    def test_gps_update(self):
        """Test updating GPS records"""
        # Update fields
        self.gps.event_description = 'Updated event description'
        self.gps.physical_violence = 'happened to someone else'
        self.gps.save()
        
        # Verify changes
        updated_gps = global_psychotrauma_screen.objects.get(pk=self.gps.pk)
        self.assertEqual(updated_gps.event_description, 'Updated event description')
        self.assertEqual(updated_gps.physical_violence, 'happened to someone else')

    def test_gps_delete(self):
        """Test deleting GPS records"""
        # Get initial count
        initial_count = global_psychotrauma_screen.objects.count()
        
        # Delete the GPS record
        self.gps.delete()
        
        # Verify deletion
        new_count = global_psychotrauma_screen.objects.count()
        self.assertEqual(new_count, initial_count - 1)
        
        # Verify considering events are also deleted
        with self.assertRaises(considering_event.DoesNotExist):
            considering_event.objects.get(pk=self.considering_event1.pk)

    def test_considering_event_relationship(self):
        """Test the relationship between GPS and considering_event"""
        # Create new GPS with multiple considering events
        new_gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='Multiple events test'
        )
        
        # Create multiple considering events
        events = [
            considering_event.objects.create(
                global_psychotrauma_screen=new_gps,
                considering_event_1='Yes',
                considering_event_2='No'
            ) for i in range(3)
        ]
        
        # Verify relationship
        related_events = considering_event.objects.filter(
            global_psychotrauma_screen=new_gps
        )
        self.assertEqual(related_events.count(), 3)

    def test_concurrent_gps_creation(self):
        """Test handling multiple GPS records for same patient"""
        # Create multiple GPS records for same patient
        gps1 = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='First event',
            event_happened='last week'
        )
        gps2 = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='Second event',
            event_happened='last month'
        )
        
        # Verify both records exist
        patient_records = global_psychotrauma_screen.objects.filter(
            details=self.patient
        ).order_by('create_date')
        self.assertEqual(patient_records.count(), 3)  # Including self.gps
        self.assertEqual(patient_records[1].event_description, 'First event')
        self.assertEqual(patient_records[2].event_description, 'Second event')
