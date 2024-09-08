from django.test import TestCase
from django.urls import reverse
from django.http import Http404

from mcc.models import MotorControlCenter as MCC
from node.models import Node

class MCCNodesViewTests(TestCase):

    def setUp(self):
        """Create test data for the MCC nodes view tests."""
        
        self.mcc = MCC.objects.create(slug='test-mcc', title='Test MCC')
        
        self.node1 = Node.objects.create(name='Node 1', mcc=self.mcc, index='node_1')
        self.node2 = Node.objects.create(name='Node 2', mcc=self.mcc, index='node_2')
        
        self.url = reverse('mcc:mcc_detail', kwargs={'mcc_slug': self.mcc.slug})

    def test_mcc_nodes_view_valid_mcc(self):
        """Test that the view returns the correct context and template for a valid MCC slug."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mcc/mcc_detail.html')
        self.assertIn('mcc', response.context)
        self.assertIn('nodes', response.context)
        self.assertEqual(response.context['mcc'], self.mcc)
        self.assertIn(self.node1, response.context['nodes'])
        self.assertIn(self.node2, response.context['nodes'])

    def test_mcc_nodes_view_invalid_mcc(self):
        """Test that the view raises a 404 error for an invalid MCC slug."""
        invalid_url = reverse('mcc:mcc_detail', kwargs={'mcc_slug': 'invalid-slug'})
        
        response = self.client.get(invalid_url)
        
        self.assertEqual(response.status_code, 404)
