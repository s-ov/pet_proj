from django.test import TestCase
from django.urls import reverse

class PreChangeDataViewTest(TestCase):
    def test_pre_change_data_view(self):
        """
        Test that the view renders the 'pre_change_data.html' template.
        """
        
        url = reverse('node:pre_change_data')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/pre_change_data.html')
