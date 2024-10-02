from django.test import TestCase
from django.urls import reverse
from node.models import Node

class DeleteNodeViewTests(TestCase):
    def setUp(self):
        """Create a sample Node instance for testing"""
        self.node = Node.objects.create(name='Норія', index='test_index') 
        self.url = reverse('node:delete_node') 

    def test_delete_node_with_valid_index(self):
        """Test valid deletion of a node"""
        response = self.client.post(self.url, {
            'name': 'Норія',
            'index': 'test_index'
        })

        self.assertRedirects(response, reverse('node:deleted_node_message'))
        with self.assertRaises(Node.DoesNotExist):
            Node.objects.get(index='test_index')  

    def test_delete_node_with_non_existent_index(self):
        """Test deletion with a non-existent node index"""
        response = self.client.post(self.url, {
            'index': 'non_existent_index'
        })

        self.assertEqual(response.status_code, 200)

    def test_delete_node_without_index(self):
        """Test deletion without providing an index"""
        response = self.client.post(self.url, {
            'index': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введіть, буль ласка, індекс.')

    def test_get_delete_node_form(self):
        """Test GET request for the delete form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/delete_node.html')
