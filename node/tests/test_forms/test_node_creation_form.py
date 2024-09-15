from django.test import TestCase
from node.forms import NodeCreationForm
from node.models import Node
from work_tower.models import WorkTowerLevel 
from mcc.models import MotorControlCenter  
from node.models import NodeMotor  

class NodeCreationFormTest(TestCase):

    def setUp(self):
        """Set up the objects needed for testing."""
        self.level = WorkTowerLevel.objects.create(level="1")
        self.motor = NodeMotor.objects.create(power=5.5)
        self.mcc = MotorControlCenter.objects.create(title="MCC 1")

    def test_form_valid_data(self):
        """Test form is valid with valid data."""
        form_data = {
            'name': 'Kонвеєр',
            'index': '1_1_1_1_1',
            'level': self.level.id,
            'motor': self.motor.id,
            'mcc': self.mcc.id,
        }
        form = NodeCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_required_fields(self):
        """Test form is invalid when required fields are missing."""
        form_data = {
            'name': '',
            'index': '',
            'level': self.level.id,
            'motor': self.motor.id,
            'mcc': self.mcc.id,
        }
        form = NodeCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('index', form.errors)

    def test_form_widgets(self):
        """Test that the form has the correct widgets."""
        form = NodeCreationForm()
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['index'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['index'].widget.attrs['placeholder'], '1_1_1_1_1')

    def test_form_labels(self):
        """Test that the form uses the correct labels."""
        form = NodeCreationForm()
        self.assertEqual(form.fields['name'].label, 'Назва')
        self.assertEqual(form.fields['index'].label, 'Індекс')
        self.assertEqual(form.fields['level'].label, 'Відмітка')
        self.assertEqual(form.fields['motor'].label, 'Мотор')
        self.assertEqual(form.fields['mcc'].label, 'MCC')

    def test_empty_index_format(self):
        """Test form raises validation error for empty index format."""
        form_data = {
            'name': 'Kонвеєр',
            'index': '',
            'level': self.level.id,
            'motor': self.motor.id,
            'mcc': self.mcc.id,
        }
        form = NodeCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('index', form.errors)
