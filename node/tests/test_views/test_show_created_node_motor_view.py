from django.test import TestCase
from django.urls import reverse
from node.models import NodeMotor

class ShowCreatedNodeMotorViewTests(TestCase):

    def setUp(self):
        """Set up url to test the view"""
        self.url = reverse('node:show_created_node_motor')  

    def test_show_created_node_motor_view_with_no_node_motors(self):
        """Test show created node motor view if there is no any motor"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Двигун не був створений.")  

    def test_show_created_node_motor_view_with_node_motors(self):
        """Test show created node motor view with valid data"""
        NodeMotor.objects.create(power=21.5)  
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 21.5)  
        self.assertTemplateUsed(response, 'node/show_created_node_motor.html')
