from django.test import TransactionTestCase, override_settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from patient.models import details, global_psychotrauma_screen, considering_event
from datetime import datetime, timedelta
import time
from contextlib import contextmanager
from patient.test_settings import DATABASES

@override_settings(DATABASES=DATABASES)
class GlobalPsychotraumaScreenValidationTests(TransactionTestCase):
    """
    Test cases for Global Psychotrauma Screen validation rules and constraints
    Using TransactionTestCase to handle database transactions better
    """
    def setUp(self):
        """Set up test data"""
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
            event_happened='last month',
            physical_violence='to yourself',
            sexual_violence='happened to someone else',
            emotional_abuse='to yourself'
        )

    def test_gps_validation(self):
        """Test GPS field validation"""
        # Test required fields
        gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_happened='last month'
        )
        self.assertIsNotNone(gps.pk)
        
        # Test boolean fields default to False
        self.assertFalse(gps.sudden_death_of_loved_one)
        self.assertFalse(gps.cause_harm_to_others)
        self.assertFalse(gps.covid)

    def test_gps_field_validations(self):
        """Test detailed field validations"""
        # Test invalid event_happened choice
        with self.assertRaises(ValidationError):
            global_psychotrauma_screen.objects.create(
                details=self.patient,
                event_happened='Invalid timeframe'
            )
        
        # Test boolean field type coercion
        gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            sudden_death_of_loved_one=True,
            cause_harm_to_others=True,
            covid=True
        )
        self.assertTrue(gps.sudden_death_of_loved_one)
        self.assertTrue(gps.cause_harm_to_others)
        self.assertTrue(gps.covid)

    def test_null_and_blank_constraints(self):
        """Test null and blank field constraints"""
        # Test required fields
        with self.assertRaises(ValidationError):
            global_psychotrauma_screen.objects.create(
                event_description='Missing patient'
                # missing details field
            )
        
        # Test optional fields are truly optional
        gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            # All other fields should be optional
        )
        self.assertIsNotNone(gps.pk)

    def test_considering_event_validations(self):
        """Test considering event validations and constraints"""
        gps = global_psychotrauma_screen.objects.create(details=self.patient)
        
        # Test maximum events per GPS
        for i in range(16):  # Try to create more than allowed
            with self.assertRaises(ValidationError) if i >= 15 else self.assertNotRaises():
                event = considering_event.objects.create(
                    global_psychotrauma_screen=gps,
                    **{f'considering_event_{i+1}': 'Yes'}
                )
        
        # Verify correct number of events were created
        self.assertEqual(considering_event.objects.filter(global_psychotrauma_screen=gps).count(), 15)

    def test_gps_date_fields(self):
        """Test GPS date-related fields"""
        # Verify create_date and update_date are set
        self.assertIsNotNone(self.gps.create_date)
        self.assertIsNotNone(self.gps.update_date)
        
        # Test date range fields
        self.gps.range_event_occurring_from = '2023-01-01'
        self.gps.range_event_occurring_to = '2023-12-31'
        self.gps.save()
        
        updated_gps = global_psychotrauma_screen.objects.get(pk=self.gps.pk)
        self.assertEqual(updated_gps.range_event_occurring_from, '2023-01-01')
        self.assertEqual(updated_gps.range_event_occurring_to, '2023-12-31')

    def test_gps_history_tracking(self):
        """Test GPS history and update tracking"""
        original_date = self.gps.update_date
        
        # Add a small delay to ensure different timestamp
        time.sleep(1)
        
        # Make changes
        self.gps.event_description = 'Updated description'
        self.gps.physical_violence = 'happened to someone else'
        self.gps.history = 'Changed description and violence status'
        self.gps.save(update_fields=['event_description', 'physical_violence', 'history'])
        
        # Verify update tracking
        updated_gps = global_psychotrauma_screen.objects.get(pk=self.gps.pk)
        self.assertNotEqual(updated_gps.update_date, original_date)
        self.assertEqual(updated_gps.history, 'Changed description and violence status')

    def test_gps_score_calculation(self):
        """Test calculation of GPS scores from considering events"""
        # Create GPS with multiple considering events
        new_gps = global_psychotrauma_screen.objects.create(
            details=self.patient,
            event_description='Score test event'
        )
        
        # Create considering events with various responses
        ce1 = considering_event.objects.create(
            global_psychotrauma_screen=new_gps,
            considering_event_1='Yes',
            considering_event_2='Yes',
            considering_event_3='No',
            considering_event_4='No',
            considering_event_5='No',
            considering_event_6='Yes',
            considering_event_7='No',
            considering_event_8='Yes',
            considering_event_9='No',
            considering_event_10='Yes',
            considering_event_11='No',
            considering_event_12='Yes',
            score_1_16=3,  # Using correct field names
            total_score=5,
        )
        
        ce2 = considering_event.objects.create(
            global_psychotrauma_screen=new_gps,
            considering_event_1='Yes',
            considering_event_2='Yes',
            score_1_16=2,
        )
        
        # Verify score calculations
        events = considering_event.objects.filter(global_psychotrauma_screen=new_gps)
        total_score_1 = sum(int(ce.score_1_16 or 0) for ce in events)
        
        self.assertEqual(total_score_1, 5)  # 3 + 2

    @contextmanager
    def assertNotRaises(self):
        """Helper method for asserting that no exception is raised"""
        try:
            yield
        except Exception as e:
            raise self.failureException(f"Exception was raised when not expected: {e}")
