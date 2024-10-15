from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from users.models import Employee

class EmployeeLoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user_profile_url = reverse('users:employee_profile', kwargs={'employee_id': 1})
        self.user = Employee.objects.create_user(cell_number='+380501234567', password='securepassword')
    
    def test_get_login_view(self):
        """
            Test GET request to login view
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/login.html')
        self.assertContains(response, 'form')
    
    def test_post_valid_login(self):
        """
            Test POST request with valid form data
        """
        data = {
            'cell_number': '+380501234567',
            'password': 'securepassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.user_profile_url)
    
    def test_post_invalid_login(self):
        """
            Test POST request with invalid form data
        """
        data = {
            'cell_number': '+380501234567',
            'password': 'invalidpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/login.html')
        self.assertContains(response, 'form')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Неправильний номер мобільного чи пароль.')

    def test_post_wrong_cell_number(self):
        """
        Test POST request with wrong cell number
        """
        data = {
            'cell_number': '+380501234568',  
            'password': 'securepassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/login.html')
        self.assertContains(response, 'form')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Неправильний номер мобільного чи пароль.')
