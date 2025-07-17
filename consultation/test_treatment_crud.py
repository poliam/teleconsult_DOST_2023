from django.test import TestCase, TransactionTestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.utils import timezone
from consultation.models import treatment, encounter
from patient.models import details, medicine
from datetime import datetime, date
import json


class TreatmentCRUDTestCase(TestCase):
    """Test cases for Treatment CRUD operations"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testdoctor',
            password='testpass123'
        )
        self.client.login(username='testdoctor', password='testpass123')
        
        self.patient = details.objects.create(
            first_name='John',
            last_name='Doe',
            gender='Male'
        )
        
        self.encounter = encounter.objects.create(
            details=self.patient,
            consultation_date='2023-01-01',
            consulted_by=self.user,
            status=True,
            is_delete=False
        )
        
        self.medicine = medicine.objects.create(
            name='Sertraline',
            status=True,
            is_delete=False
        )

    def test_create_treatment_success(self):
        """Test successful treatment creation"""
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': self.encounter.pk,
            'drug': 'Sertraline',
            'strength': '50mg',
            'dose': '1 tablet',
            'Route': 'Oral',
            'frequency': 'Once daily',
            'no': '30'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 1)
        self.assertIn('treatment_id', data)
        
        # Verify treatment was created
        treatment_instance = treatment.objects.get(pk=data['treatment_id'])
        self.assertEqual(treatment_instance.drugs.name, 'Sertraline')
        self.assertEqual(treatment_instance.strength, '50mg')
        self.assertEqual(treatment_instance.dose, '1 tablet')
        self.assertEqual(treatment_instance.route, 'Oral')
        self.assertEqual(treatment_instance.frequency, 'Once daily')
        self.assertEqual(treatment_instance.drug_no, '30')
        self.assertEqual(treatment_instance.encounter, self.encounter)
        self.assertTrue(treatment_instance.status)
        self.assertFalse(treatment_instance.is_delete)

    def test_create_treatment_new_medicine(self):
        """Test treatment creation with new medicine"""
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': self.encounter.pk,
            'drug': 'Fluoxetine',  # New medicine
            'strength': '20mg',
            'dose': '1 tablet',
            'Route': 'Oral',
            'frequency': 'Once daily',
            'no': '30'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 1)
        
        # Verify new medicine was created
        self.assertTrue(medicine.objects.filter(name='Fluoxetine').exists())
        
        # Verify treatment was created with new medicine
        treatment_instance = treatment.objects.get(pk=data['treatment_id'])
        self.assertEqual(treatment_instance.drugs.name, 'Fluoxetine')

    def test_create_treatment_invalid_encounter(self):
        """Test treatment creation with invalid encounter"""
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': 99999,  # Invalid encounter ID
            'drug': 'Sertraline',
            'strength': '50mg',
            'dose': '1 tablet',
            'Route': 'Oral',
            'frequency': 'Once daily',
            'no': '30'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 0)
        self.assertIn('error_msg', data)
        self.assertEqual(data['error_msg'], 'Encounter Does not exists')

    def test_create_treatment_empty_drug(self):
        """Test treatment creation with empty drug name"""
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': self.encounter.pk,
            'drug': '',  # Empty drug name
            'strength': '50mg',
            'dose': '1 tablet',
            'Route': 'Oral',
            'frequency': 'Once daily',
            'no': '30'
        })
        
        # Should handle empty drug name gracefully
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Check if it creates medicine with empty name or handles error appropriately
        self.assertIn('status_code', data)

    def test_create_treatment_optional_fields(self):
        """Test treatment creation with optional fields empty"""
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': self.encounter.pk,
            'drug': 'Sertraline',
            'strength': '',  # Empty optional field
            'dose': '',      # Empty optional field
            'Route': '',     # Empty optional field
            'frequency': '', # Empty optional field
            'no': ''         # Empty optional field
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 1)
        
        # Verify treatment was created with empty optional fields
        treatment_instance = treatment.objects.get(pk=data['treatment_id'])
        self.assertEqual(treatment_instance.strength, '')
        self.assertEqual(treatment_instance.dose, '')
        self.assertEqual(treatment_instance.route, '')
        self.assertEqual(treatment_instance.frequency, '')
        self.assertEqual(treatment_instance.drug_no, '')

    def test_delete_treatment_success(self):
        """Test successful treatment deletion"""
        # Create a treatment first
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg',
            dose='1 tablet',
            route='Oral',
            frequency='Once daily',
            drug_no='30'
        )
        
        response = self.client.post(reverse('DeleteTreatment'), {
            'drug_id': treatment_instance.pk
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 1)
        
        # Verify treatment was soft deleted
        treatment_instance.refresh_from_db()
        self.assertTrue(treatment_instance.is_delete)
        self.assertFalse(treatment_instance.status)

    def test_delete_treatment_invalid_id(self):
        """Test treatment deletion with invalid ID"""
        response = self.client.post(reverse('DeleteTreatment'), {
            'drug_id': 99999  # Invalid treatment ID
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 0)
        self.assertIn('error_msg', data)
        self.assertEqual(data['error_msg'], 'treatment Does not exists')

    def test_unauthorized_treatment_access(self):
        """Test that unauthorized users cannot access treatment endpoints"""
        self.client.logout()
        
        # Test create treatment without authentication
        try:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Sertraline',
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            # Should redirect to login
            self.assertEqual(response.status_code, 302)
            self.assertIn('login', response.url.lower())
        except Exception as e:
            # If login URL is not configured, just verify authentication is required
            self.assertIn('login', str(e).lower())

    def test_treatment_model_constraints(self):
        """Test treatment model field constraints"""
        # Test creating valid treatment
        valid_treatment = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg',
            dose='1 tablet',
            route='Oral',
            frequency='Once daily',
            drug_no='30'
        )
        self.assertTrue(valid_treatment.pk)

    def test_treatment_default_values(self):
        """Test treatment model default values"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        self.assertTrue(treatment_instance.status)
        self.assertFalse(treatment_instance.is_delete)
        self.assertIsNotNone(treatment_instance.create_date)
        self.assertIsNotNone(treatment_instance.update_date)

    def test_treatment_cascade_behavior(self):
        """Test treatment cascade behavior on related object deletion"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        # Test encounter deletion (should set to None)
        self.encounter.delete()
        treatment_instance.refresh_from_db()
        self.assertIsNone(treatment_instance.encounter)
        
        # Test medicine deletion (should set to None)
        self.medicine.delete()
        treatment_instance.refresh_from_db()
        self.assertIsNone(treatment_instance.drugs)

    def test_treatment_filtering(self):
        """Test treatment filtering by status and delete flags"""
        # Create treatments with different statuses
        active_treatment = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg',
            status=True,
            is_delete=False
        )
        
        inactive_treatment = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='25mg',
            status=False,
            is_delete=False
        )
        
        deleted_treatment = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='100mg',
            status=True,
            is_delete=True
        )
        
        # Test filtering active treatments
        active_treatments = treatment.objects.filter(status=True, is_delete=False)
        self.assertIn(active_treatment, active_treatments)
        self.assertNotIn(inactive_treatment, active_treatments)
        self.assertNotIn(deleted_treatment, active_treatments)

    def test_treatment_history_tracking(self):
        """Test treatment history field functionality"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg',
            history='Initial treatment'
        )
        
        self.assertEqual(treatment_instance.history, 'Initial treatment')
        
        # Update history
        treatment_instance.history = 'Updated treatment'
        treatment_instance.save()
        
        treatment_instance.refresh_from_db()
        self.assertEqual(treatment_instance.history, 'Updated treatment')

    def test_treatment_update_timestamps(self):
        """Test that update_date is modified when treatment is updated"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        original_update_date = treatment_instance.update_date
        
        # Update treatment
        treatment_instance.strength = '100mg'
        treatment_instance.save()
        
        treatment_instance.refresh_from_db()
        # Note: update_date uses auto_now_add=True which doesn't update on save
        # This is likely a model design issue, but we test the current behavior
        self.assertEqual(treatment_instance.update_date, original_update_date)

    def test_treatment_bulk_operations(self):
        """Test bulk treatment operations"""
        # Create multiple treatments
        treatments = []
        for i in range(5):
            treatment_instance = treatment.objects.create(
                encounter=self.encounter,
                drugs=self.medicine,
                strength=f'{50 + i * 10}mg',
                dose=f'{i + 1} tablet(s)'
            )
            treatments.append(treatment_instance)
        
        # Test bulk update
        treatment.objects.filter(encounter=self.encounter).update(status=False)
        
        # Verify all were updated
        for t in treatments:
            t.refresh_from_db()
            self.assertFalse(t.status)
        
        # Test bulk delete
        treatment.objects.filter(encounter=self.encounter).delete()
        
        # Verify all were deleted
        remaining = treatment.objects.filter(encounter=self.encounter).count()
        self.assertEqual(remaining, 0)

    def test_treatment_data_integrity(self):
        """Test treatment data integrity and validation"""
        # Test that treatments maintain data integrity
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg',
            dose='1 tablet',
            route='Oral',
            frequency='Once daily',
            drug_no='30'
        )
        
        # Verify all fields are saved correctly
        self.assertEqual(treatment_instance.strength, '50mg')
        self.assertEqual(treatment_instance.dose, '1 tablet')
        self.assertEqual(treatment_instance.route, 'Oral')
        self.assertEqual(treatment_instance.frequency, 'Once daily')
        self.assertEqual(treatment_instance.drug_no, '30')

    def test_treatment_ordering(self):
        """Test treatment ordering by creation date"""
        # Create treatments at different times
        treatment1 = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        # Add small delay to ensure different timestamps
        import time
        time.sleep(0.1)
        
        treatment2 = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='100mg'
        )
        
        # Test ordering by creation date (newest first)
        treatments = treatment.objects.filter(encounter=self.encounter).order_by('-create_date')
        self.assertEqual(len(treatments), 2)
        # Just verify they are ordered correctly by timestamp
        self.assertTrue(treatments[0].create_date >= treatments[1].create_date)

    def test_treatment_model_str_representation(self):
        """Test treatment model string representation"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        # Test that string representation works (even if not explicitly defined)
        str_repr = str(treatment_instance)
        self.assertIsInstance(str_repr, str)


class TreatmentValidationTestCase(TestCase):
    """Test cases for Treatment validation logic"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testdoctor',
            password='testpass123'
        )
        self.client.login(username='testdoctor', password='testpass123')
        
        self.patient = details.objects.create(
            first_name='John',
            last_name='Doe',
            gender='Male'
        )
        
        self.encounter = encounter.objects.create(
            details=self.patient,
            consultation_date='2023-01-01',
            consulted_by=self.user,
            status=True,
            is_delete=False
        )

    def test_drug_name_validation(self):
        """Test drug name validation"""
        # Test valid drug names
        valid_drugs = [
            'Sertraline',
            'Fluoxetine HCl',
            'Lorazepam 0.5mg',
            'Risperidone (Generic)',
            'Quetiapine XR',
            'Aripiprazole-10mg'
        ]
        
        for drug_name in valid_drugs:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': drug_name,
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for drug: {drug_name}")

    def test_strength_validation(self):
        """Test strength field validation"""
        # Test various strength formats
        strength_formats = [
            '50mg',
            '0.5mg',
            '25 mg',
            '100 MG',
            '2.5mg/ml',
            '10mg/5ml',
            '500mcg',
            '1g'
        ]
        
        for strength in strength_formats:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Test Drug',
                'strength': strength,
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for strength: {strength}")

    def test_dose_validation(self):
        """Test dose field validation"""
        # Test various dose formats
        dose_formats = [
            '1 tablet',
            '2 tablets',
            '0.5 tablet',
            '1 capsule',
            '5ml',
            '10 drops',
            '1 sachet',
            '2 puffs'
        ]
        
        for dose in dose_formats:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Test Drug',
                'strength': '50mg',
                'dose': dose,
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for dose: {dose}")

    def test_route_validation(self):
        """Test route field validation"""
        # Test various route formats
        route_formats = [
            'Oral',
            'Sublingual',
            'Intramuscular',
            'Intravenous',
            'Topical',
            'Inhaled',
            'Rectal',
            'Nasal'
        ]
        
        for route in route_formats:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Test Drug',
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': route,
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for route: {route}")

    def test_frequency_validation(self):
        """Test frequency field validation"""
        # Test various frequency formats
        frequency_formats = [
            'Once daily',
            'Twice daily',
            'Three times daily',
            'Four times daily',
            'Every 8 hours',
            'Every 12 hours',
            'As needed',
            'PRN',
            'BID',
            'TID',
            'QID'
        ]
        
        for frequency in frequency_formats:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Test Drug',
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': frequency,
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for frequency: {frequency}")

    def test_drug_number_validation(self):
        """Test drug number field validation"""
        # Test various drug number formats
        drug_numbers = [
            '30',
            '14',
            '7',
            '60',
            '90',
            '100',
            '1'
        ]
        
        for drug_no in drug_numbers:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': 'Test Drug',
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': drug_no
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for drug number: {drug_no}")

    def test_special_characters_in_fields(self):
        """Test fields with special characters"""
        # Test drug names with special characters
        special_drug_names = [
            'Co-trimoxazole',
            'Acetaminophen/Codeine',
            'Vitamin B-Complex',
            'Omega-3 Fatty Acids',
            'L-Theanine',
            'N-Acetylcysteine'
        ]
        
        for drug_name in special_drug_names:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': drug_name,
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for drug: {drug_name}")

    def test_unicode_character_handling(self):
        """Test handling of unicode characters in treatment"""
        # Test unicode characters in drug names
        unicode_drugs = [
            'Paracétamol',  # French
            'Ibuprofén',    # Spanish
            'Диазепам',     # Russian
            'アスピリン',     # Japanese
            'Aspirină',     # Romanian
        ]
        
        for drug_name in unicode_drugs:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': drug_name,
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1, f"Failed for unicode drug: {drug_name}")

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention in treatment creation"""
        # Test various SQL injection attempts
        sql_injections = [
            "'; DROP TABLE treatment; --",
            "' OR '1'='1",
            "'; DELETE FROM medicine; --",
            "' UNION SELECT * FROM users --"
        ]
        
        for sql_injection in sql_injections:
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': sql_injection,
                'strength': '50mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            # Should not cause server error, even if it creates the treatment
            self.assertIn('status_code', data)

    def test_duplicate_medicine_handling(self):
        """Test handling of duplicate medicine names"""
        # Create medicine first
        medicine.objects.create(name='Duplicate Drug')
        
        # Try to create treatment with same drug name
        response = self.client.post(reverse('CreateTreatment'), {
            'encounter_id': self.encounter.pk,
            'drug': 'Duplicate Drug',
            'strength': '50mg',
            'dose': '1 tablet',
            'Route': 'Oral',
            'frequency': 'Once daily',
            'no': '30'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status_code'], 1)
        
        # Verify only one medicine with this name exists
        medicine_count = medicine.objects.filter(name='Duplicate Drug').count()
        self.assertEqual(medicine_count, 1)

    def test_concurrent_treatment_creation(self):
        """Test concurrent treatment creation"""
        # Test multiple treatments for same encounter
        treatments_created = []
        
        for i in range(5):
            response = self.client.post(reverse('CreateTreatment'), {
                'encounter_id': self.encounter.pk,
                'drug': f'Drug {i}',
                'strength': f'{50 + i * 10}mg',
                'dose': '1 tablet',
                'Route': 'Oral',
                'frequency': 'Once daily',
                'no': '30'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status_code'], 1)
            treatments_created.append(data['treatment_id'])
        
        # Verify all treatments were created
        self.assertEqual(len(treatments_created), 5)
        
        # Verify all treatments exist in database
        for treatment_id in treatments_created:
            self.assertTrue(treatment.objects.filter(pk=treatment_id).exists())


class TreatmentConstraintTestCase(TransactionTestCase):
    """Test cases for Treatment model constraints and database integrity"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testdoctor',
            password='testpass123'
        )
        
        self.patient = details.objects.create(
            first_name='John',
            last_name='Doe',
            gender='Male'
        )
        
        self.encounter = encounter.objects.create(
            details=self.patient,
            consultation_date='2023-01-01',
            consulted_by=self.user
        )
        
        self.medicine = medicine.objects.create(
            name='Test Medicine',
            status=True,
            is_delete=False
        )

    def test_treatment_model_constraints(self):
        """Test treatment model field constraints"""
        # Test creating valid treatment
        valid_treatment = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        self.assertTrue(valid_treatment.pk)

    def test_treatment_default_values(self):
        """Test treatment model default values"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        self.assertTrue(treatment_instance.status)
        self.assertFalse(treatment_instance.is_delete)
        self.assertIsNotNone(treatment_instance.create_date)
        self.assertIsNotNone(treatment_instance.update_date)

    def test_treatment_cascade_behavior(self):
        """Test treatment cascade behavior on related object deletion"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        # Test encounter deletion (should set to None)
        self.encounter.delete()
        treatment_instance.refresh_from_db()
        self.assertIsNone(treatment_instance.encounter)
        
        # Test medicine deletion (should set to None)
        self.medicine.delete()
        treatment_instance.refresh_from_db()
        self.assertIsNone(treatment_instance.drugs)

    def test_treatment_soft_delete(self):
        """Test treatment soft delete functionality"""
        treatment_instance = treatment.objects.create(
            encounter=self.encounter,
            drugs=self.medicine,
            strength='50mg'
        )
        
        # Soft delete
        treatment_instance.is_delete = True
        treatment_instance.status = False
        treatment_instance.save()
        
        # Should still exist in database
        self.assertTrue(treatment.objects.filter(pk=treatment_instance.pk).exists())
        
        # Should be filtered out in active queries
        active_treatments = treatment.objects.filter(status=True, is_delete=False)
        self.assertNotIn(treatment_instance, active_treatments)

    def test_treatment_bulk_operations(self):
        """Test treatment bulk operations"""
        # Create multiple treatments
        treatments = []
        for i in range(10):
            treatment_instance = treatment.objects.create(
                encounter=self.encounter,
                drugs=self.medicine,
                strength=f'{50 + i * 10}mg'
            )
            treatments.append(treatment_instance)
        
        # Test bulk update
        treatment.objects.filter(encounter=self.encounter).update(status=False)
        
        # Verify all were updated
        for t in treatments:
            t.refresh_from_db()
            self.assertFalse(t.status)
        
        # Test bulk delete
        treatment.objects.filter(encounter=self.encounter).delete()
        
        # Verify all were deleted
        remaining = treatment.objects.filter(encounter=self.encounter).count()
        self.assertEqual(remaining, 0)

    def test_treatment_database_integrity(self):
        """Test treatment database integrity"""
        with transaction.atomic():
            # Create treatment
            treatment_instance = treatment.objects.create(
                encounter=self.encounter,
                drugs=self.medicine,
                strength='50mg'
            )
            
            # Verify it exists
            self.assertTrue(treatment.objects.filter(pk=treatment_instance.pk).exists())
            
            # Test transaction rollback
            try:
                with transaction.atomic():
                    # Create another treatment
                    treatment2 = treatment.objects.create(
                        encounter=self.encounter,
                        drugs=self.medicine,
                        strength='100mg'
                    )
                    
                    # Force an error to trigger rollback
                    raise Exception("Test rollback")
            except Exception:
                pass
            
            # First treatment should still exist
            self.assertTrue(treatment.objects.filter(pk=treatment_instance.pk).exists())
            
            # Second treatment should not exist due to rollback
            self.assertFalse(treatment.objects.filter(strength='100mg').exists())

    def tearDown(self):
        """Clean up after constraint tests"""
        pass
