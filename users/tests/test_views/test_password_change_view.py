from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from users.models import Employee

class PasswordChangeViewTest(TestCase):
    """Tests for password change view."""
    def setUp(self):
        """Set up a test user and log in."""
        self.user = Employee.objects.create_user(
            cell_number='+380501234567',
            password='old_password',
        )
        self.client.login(cell_number='+380501234567', password='old_password')
        self.url = reverse('users:password_change')

    def test_password_change_view_get(self):
        """Test GET request to password change view returns correct template."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration/password_change.html')

    def test_password_change_view_post_valid(self):
        """Test POST request with valid data changes the user's password and redirects."""
        response = self.client.post(self.url, {
            'old_password': 'old_password',
            'new_password1': 'new_password123',
            'new_password2': 'new_password123'
        })
        self.user.refresh_from_db()
        self.assertTrue(check_password('new_password123', self.user.password))
        self.assertRedirects(response, reverse('users:password_change_done'))

    def test_password_change_view_post_invalid(self):
        """Test POST request with invalid data does not change the password."""
        response = self.client.post(self.url, {
            'old_password': 'wrong_password',
            'new_password1': 'new_password123',
            'new_password2': 'new_password123'
        })
        self.user.refresh_from_db()
        self.assertFalse(check_password('wrong_password', self.user.password))
        self.assertFormError(response, 'form', 'old_password', 'Старий пароль було введено неправильно. Будь ласка, введіть його знову.')

    def test_password_change_view_post_mismatched_passwords(self):
        """Test POST request with mismatched new passwords does not change the password."""
        response = self.client.post(self.url, {
            'old_password': 'old_password',
            'new_password1': 'new_password123',
            'new_password2': 'different_password'
        })
        self.user.refresh_from_db()
        self.assertFalse(check_password('different_password', self.user.password))
        self.assertFormError(response, 'form', 'new_password2', 'Паролі не збігаються')
