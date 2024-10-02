from django.test import TestCase
from django.urls import reverse
from node.models import Node, NodeMotor

class SearchNodeViewTest(TestCase):

    def setUp(self):
        """Set up a NodeMotor and Node instance for valid tests"""
        self.motor = NodeMotor.objects.create(
            power=10.5, round_per_minute=3000, connection="▲", amperage=15.5
        )
        self.node = Node.objects.create(
            name="Засувка", index="1_1_1_1", motor=self.motor
        )

    def test_search_node_view_get_request(self):
        """
        Test GET request to the search node view returns the search form.
        """
        response = self.client.get(reverse('node:search_node'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/search_node_form.html')
        self.assertNotIn('error', response.context)

    def test_search_node_view_post_no_index(self):
        """
        Test POST request with no index returns an error message.
        """
        response = self.client.post(reverse('node:search_node'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/search_node_form.html')
        self.assertContains(response, 'Введіть, буль ласка, індекс.')

    def test_search_node_view_post_valid_index(self):
        """
        Test POST request with a valid index returns the node and motor details.
        """
        response = self.client.post(reverse('node:search_node'), {'index': self.node.index})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/search_node_form.html')
        self.assertContains(response, self.node.index)
        self.assertIn('node', response.context)
        self.assertIn('motor', response.context)

    def test_search_node_view_post_invalid_index(self):
        """
        Test POST request with an invalid index returns an error message.
        """
        response = self.client.post(reverse('node:search_node'), {'index': 'invalid_index'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/search_node_form.html')
        self.assertNotIn('node', response.context)
        self.assertNotIn('motor', response.context)

