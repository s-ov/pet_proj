from django.test import TestCase
from django.urls import reverse
from node.forms import NodeMotorCreationForm
from node.models import NodeMotor

class CreateNodeMotorViewTest(TestCase):

    def test_create_node_motor_view_get_request(self):
        """
        Test that the GET request returns the NodeMotor creation form.
        """
        response = self.client.get(reverse('node:create_node_motor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node_motor.html')
        self.assertIsInstance(response.context['form'], NodeMotorCreationForm)

    def test_create_node_motor_view_post_valid_data(self):
        """
        Test POST request with valid data creates a NodeMotor and redirects.
        """
        valid_data = {
            'power': 15.5,
            'round_per_minute': 3000,
            'connection': '▲',
            'amperage': 10.5,
        }
        response = self.client.post(reverse('node:create_node_motor'), data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('node:show_created_node_motor'))

        motor = NodeMotor.objects.last()
        self.assertIsNotNone(motor)
        self.assertEqual(motor.power, 15.5)
        self.assertEqual(motor.round_per_minute, 3000)
        self.assertEqual(motor.connection, '▲')
        self.assertEqual(motor.amperage, 10.5)

    def test_create_node_motor_view_post_invalid_data(self):
        """
        Test POST request with invalid data shows form errors.
        """
        invalid_data = {
            'power': '',  
            'round_per_minute': '',
            'connection': '',
            'amperage': '',
        }
        response = self.client.post(reverse('node:create_node_motor'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/create_node_motor.html')
        self.assertIsInstance(response.context['form'], NodeMotorCreationForm)
        self.assertTrue(response.context['form'].errors)

        motor_count = NodeMotor.objects.count()
        self.assertEqual(motor_count, 0)
