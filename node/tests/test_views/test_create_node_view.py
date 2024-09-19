from django.test import TestCase
from django.urls import reverse
from node.models import Node, NodeMotor
from node.forms import NodeCreationForm
from work_tower.models import WorkTowerLevel
from mcc.models import MotorControlCenter

class CreateNodeViewTest(TestCase):

    def setUp(self):
        """Set up any required foreign key relationships here"""
        self.level = WorkTowerLevel.objects.create(level='1')
        self.motor = NodeMotor.objects.create(power=7.5, round_per_minute=1450, connection='✳', amperage=15.5)
        self.mcc = MotorControlCenter.objects.create(title='MCC 1')
        self.url = reverse('node:create_node')

    def test_get_create_node_view(self):
        """Test that the view returns the correct template with a GET request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node.html')
        self.assertIsInstance(response.context['form'], NodeCreationForm)

    def test_post_create_node_view_success(self):
        """Test that the view processes valid form data and redirects after a successful POST."""
        form_data = {
            'name': 'Норія',
            'index': '1_1_1_1_1',
            'level': self.level.id,
            'motor': self.motor.id,
            'mcc': self.mcc.id,
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('node:show_created_node'))

        self.assertTrue(Node.objects.filter(index='1_1_1_1_1').exists())

    def test_post_create_node_view_invalid(self):
        """Test that invalid form data results in the form being re-rendered with errors."""
        form_data = {
            'name': '',
            'index': '',
            'level': '',
            'motor': '',
            'mcc': '',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node.html')

        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('name', response.context['form'].errors)
        self.assertIn('index', response.context['form'].errors)
