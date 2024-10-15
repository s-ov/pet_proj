from django.test import TestCase, Client
from django.urls import reverse

from users.employee_forms import EmployeeRegistrationForm
from users.models import Employee


class EmployeeRegisterViewTests(TestCase):
    def setUp(self):
        """
            Create a client instance and URL for use in tests.
        """
        self.client = Client()
        self.register_url = reverse('users:register') 

    def test_get_register_view(self):
        """
            Test GET request to registration page
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/register.html')
        self.assertIsInstance(response.context['form'], EmployeeRegistrationForm)

    def test_post_valid_form(self):
        """
            Test POST request with valid form data
        """
        data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'admission_group': 'І-ша група з електробезпеки',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(Employee.objects.filter(cell_number='+380501234567').exists())


    def test_post_invalid_form(self):
        """
            Test POST request with invalid form data
        """
        data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'admission_group': 'І-ша група з електробезпеки',
            'password': 'securepassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/register.html')
        self.assertFormError(response, 'form', 'confirm_password', 'Це поле обов\'язкове.')
        
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)

    def test_post_mismatched_passwords(self):
        """
            Test POST request with mismatched passwords
        """
        data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'admission_group': 'І-ша група з електробезпеки',
            'password': 'securepassword',
            'confirm_password': 'differentpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'users/registration/register.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Паролі не співпадають.', form.non_field_errors())