from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class UserUpdateViewTests(TestCase):
    """ 
        Test suite for the user update view 
    """

    def setUp(self):
        """ 
            Create a test user 
        """
        self.user = CustomUser.objects.create_user(
            cell_number='+380501234567',
            password='password123',
        )
        self.client.login(cell_number='+380501234567', password='password123')

    def test_user_update_view_get(self):
        """ 
            Test the GET request to the update view 
        """
        response = self.client.get(reverse('users:update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update_mobile.html')
        self.assertContains(response, '+380501234567')

    def test_user_update_view_with_valid_data(self):
        """ 
            Test the POST request with valid data 
        """
        response = self.client.post(reverse('users:update_profile'), {
            'cell_number': '+380507654321',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.cell_number, '+380507654321')

    def test_user_update_view_with_invalid_data(self):
        """ 
            Test the POST request with invalid data 
        """
        response = self.client.post(reverse('users:update_profile'), {
            'cell_number': 'invalid_number',  
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update_mobile.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ваші дані не вдалося оновити. Будь ласка, перевірте пароль.')
