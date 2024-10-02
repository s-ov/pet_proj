from django.test import TestCase
from django.urls import reverse

from node.models import Node
from node.forms import NodeCreationForm
from mcc.models import MotorControlCenter as MCC

class UpdateNodeViewTests(TestCase):
    def setUp(self):
        """Create a data for testing"""
        self.mcc = MCC.objects.create(title='MCC-1', slug='mcc-1',)
        self.node = Node.objects.create(name='Норія', index='1_1',  mcc=self.mcc,)
        self.url = reverse('node:update_node')


    def test_update_node_without_index(self):
        """Test update without providing index"""
        response = self.client.post(self.url, {
            'update': 'Update'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введіть, буль ласка, індекс.')

    def test_get_update_node_form(self):
        """Test GET request for the update form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/update_node_form.html')

    def test_update_node_non_existent(self):
        """Test update with a non-existent node"""
        response = self.client.post(self.url, {
            'index': 'non_existent_index',
            'update': 'Update'
        })
        
        self.assertEqual(response.status_code, 200)
