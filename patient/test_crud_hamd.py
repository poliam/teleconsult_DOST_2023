from django.test import TestCase
from patient.models import details, hamd

class HamdCRUDTest(TestCase):
    def setUp(self):
        self.patient = details.objects.create(first_name='Test', last_name='Patient')
        self.hamd_data = {
            'details': self.patient,
            'score': '10',
            'total_score': '20',
            'depressed_mood': '2',
            'feeling_of_guilt': '1',
        }

    def test_create_hamd(self):
        record = hamd.objects.create(**self.hamd_data)
        self.assertIsNotNone(record.id)
        self.assertEqual(record.score, '10')

    def test_read_hamd(self):
        record = hamd.objects.create(**self.hamd_data)
        fetched = hamd.objects.get(id=record.id)
        self.assertEqual(fetched.depressed_mood, '2')

    def test_update_hamd(self):
        record = hamd.objects.create(**self.hamd_data)
        record.score = '15'
        record.save()
        updated = hamd.objects.get(id=record.id)
        self.assertEqual(updated.score, '15')

    def test_delete_hamd(self):
        record = hamd.objects.create(**self.hamd_data)
        record.delete()
        with self.assertRaises(hamd.DoesNotExist):
            hamd.objects.get(id=record.id)

    def test_soft_delete_hamd(self):
        record = hamd.objects.create(**self.hamd_data)
        record.is_delete = 1
        record.save()
        self.assertFalse(hamd.objects.filter(id=record.id, is_delete=0).exists())
        self.assertTrue(hamd.objects.filter(id=record.id).exists())

#python manage.py test patient.test_crud_hamd 