from django.test import TestCase
from django.urls import reverse
from node.models import Node
from work_tower.models import WorkTowerLevel

class GetLevelNodesViewTests(TestCase):

    def setUp(self):
        """Set up data for testing"""
        self.url = reverse('node:get_level_nodes')  
        self.level1 = WorkTowerLevel.objects.create(level="1")
        self.level2 = WorkTowerLevel.objects.create(level="2")

    def test_get_level_nodes_view_no_level_post(self):
        """Test get level nodes view if there is no level input"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введіть, буль ласка, відмітку.")

    def test_get_level_nodes_view_invalid_level(self):
        """Test get level nodes view with invalid level input"""
        response = self.client.post(self.url, data={'level': '999'})
        self.assertEqual(response.status_code, 404)

    def test_get_level_nodes_view_no_nodes_for_level(self):
        """Test get level nodes view without nodes on the level"""
        response = self.client.post(self.url, data={'level': self.level2.id})
        self.assertEqual(response.status_code, 200)
        
    def test_get_level_nodes_view_with_nodes(self):
        """Test get level nodes view with nodes on the level"""
        Node.objects.create(name="Норія", index='1_1', level=self.level1)
        response = self.client.post(self.url, data={'level': self.level1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Норія")  
        self.assertContains(response, self.level1.level)

    def test_get_level_nodes_view_renders_correct_template(self):
        """Test get level nodes view whether it renders correct template"""
        response = self.client.post(self.url, data={'level': self.level1.id})
        self.assertTemplateUsed(response, 'node/level_nodes.html')
