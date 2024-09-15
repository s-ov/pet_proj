from django.test import TestCase
from node.forms import NodeMotorCreationForm
from node.models import NodeMotor

class NodeMotorCreationFormTest(TestCase):

    def test_form_valid_data(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'power': 7.5,
            'round_per_minute': 1450,
            'connection': '✳',
            'amperage': 15.5,
        }
        form = NodeMotorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_required_fields(self):
        """Test that the form is invalid when required fields are missing."""
        form_data = {
            'power': '',
            'round_per_minute': '',
            'connection': '',
            'amperage': '',
        }
        form = NodeMotorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('power', form.errors)
        self.assertIn('round_per_minute', form.errors)
        self.assertIn('connection', form.errors)
        self.assertIn('amperage', form.errors)

    def test_form_invalid_non_numeric_fields(self):
        """Test that the form is invalid when numeric fields have non-numeric data."""
        form_data = {
            'power': 'invalid',
            'round_per_minute': 'invalid',
            'connection': 'Зірка',
            'amperage': 'invalid',
        }
        form = NodeMotorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('power', form.errors)
        self.assertIn('round_per_minute', form.errors)
        self.assertIn('amperage', form.errors)

    def test_form_labels(self):
        """Test that the form uses the correct labels."""
        form = NodeMotorCreationForm()
        self.assertEqual(form.fields['power'].label, 'Потужність')
        self.assertEqual(form.fields['round_per_minute'].label, 'Обороти на хвилину')
        self.assertEqual(form.fields['connection'].label, 'Тип з\'єднання')
        self.assertEqual(form.fields['amperage'].label, 'Сила струму')
