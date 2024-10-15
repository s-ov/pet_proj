from django.test import TestCase
from django.urls import reverse

from users.models import Employee

class EmployeeLogoutViewTest(TestCase):
    """
        Test logout view.
    """
    
    def setUp(self):
        """
            Create a test user and log in.
        """
        self.user = Employee.objects.create_user(
            cell_number='+380501234567',
            password='password123'
        )
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.home_url = reverse('main_page')
    
    def test_logout_redirects_to_home(self):
        """
            Test that the user is logged out and redirected to the home page.
        """
        self.client.login(cell_number='+380501234567', password='password123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        
        response = self.client.get(self.home_url)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_logout_when_not_logged_in(self):
        """
            Test that the user is not logged in and redirected to the home page.
        """
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
