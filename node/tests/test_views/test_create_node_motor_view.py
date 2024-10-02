from django.test import TestCase
from django.urls import reverse
from node.models import NodeMotor
from node.forms import NodeMotorCreationForm

class CreateNodeMotorViewTest(TestCase):

    def test_get_create_node_motor_view(self):
        """Test that the view returns the correct template with a GET request."""
        response = self.client.get(reverse('node:create_node_motor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node_motor.html')
        self.assertIsInstance(response.context['form'], NodeMotorCreationForm)

    def test_post_create_node_motor_view_success(self):
        """Test that the view processes valid form data and redirects after a successful POST."""
        form_data = {
            'power': 7.5,
            'round_per_minute': 1450,
            'connection': '✳',
            'amperage': 15.5,
        }
        response = self.client.post(reverse('node:create_node_motor'), data=form_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('node:show_created_node_motor'))
        
        self.assertTrue(NodeMotor.objects.filter(power=7.5, round_per_minute=1450).exists())

    def test_post_create_node_motor_view_invalid(self):
        """Test that invalid form data results in the form being re-rendered with errors."""
        form_data = {
            'power': '',
            'round_per_minute': '',
            'connection': '',
            'amperage': '',
        }
        response = self.client.post(reverse('node:create_node_motor'), data=form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node_motor.html')
        
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('power', response.context['form'].errors)
        self.assertIn('round_per_minute', response.context['form'].errors)
        self.assertIn('connection', response.context['form'].errors)
        self.assertIn('amperage', response.context['form'].errors)
