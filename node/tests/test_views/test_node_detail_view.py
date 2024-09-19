from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from node.models import Node, NodeMotor

class NodeDetailViewTest(TestCase):
    
    def setUp(self):
        """Create a NodeMotor instance for the Node"""
        self.motor = NodeMotor.objects.create(
            power=10.5, 
            round_per_minute=1500, 
            connection="✳", 
            amperage=20.0
        )

        self.node = Node.objects.create(
            name="Kонвеєр",
            index="1_1_1_1_1",
            motor=self.motor
        )
        self.url = reverse('node:node_detail', kwargs={'node_id': self.node.id})
    
    def test_node_detail_view_success(self):
        """Test that node_detail_view returns a 200 status for a valid node ID."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/node_detail.html')
        self.assertContains(response, self.node.index)

    def test_node_detail_view_invalid_node_id(self):
        """Test that node_detail_view returns a 404 status for an invalid node ID."""
        url = reverse('node:node_detail', kwargs={'node_id': 9999})  
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_node_detail_view_context(self):
        """Test that the context contains the correct node and motor details."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.context['node'], self.node)
        self.assertEqual(response.context['motor'], self.motor)
    
    def test_node_detail_view_no_motor(self):
        """Test that the view handles a Node without a motor."""

        node_without_motor = Node.objects.create(
            name="Норія",
            index="1_1_1_1_2"
        )
        
        url = reverse('node:node_detail', kwargs={'node_id': node_without_motor.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, node_without_motor.index)
        self.assertIsNone(response.context['motor'])
