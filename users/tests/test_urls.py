from django.test import TestCase
from django.urls import reverse, resolve
from users.employee_views import ( 
    employee_register_view,
    employee_login_view,
    employee_profile_view,
    employee_update_view,
    password_change_view,
    employee_logout_view,
    delete_employee_view,
    electricians_list_view,
    employee_tasks_view
)
from django.contrib.auth.views import PasswordChangeDoneView


class UsersURLTests(TestCase):

    def test_register_url_is_resolved(self):
        """Test that the register URL resolves to the correct view."""
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, employee_register_view)

    def test_login_url_is_resolved(self):
        """Test that the login URL resolves to the correct view."""
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, employee_login_view)

    def test_logout_url_is_resolved(self):
        """Test that the logout URL resolves to the correct view."""
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, employee_logout_view)

    def test_employee_profile_url_is_resolved(self):
        """Test that the employee profile URL resolves to the correct view."""
        url = reverse('users:employee_profile', args=[1])
        self.assertEqual(resolve(url).func, employee_profile_view)

    def test_update_profile_url_is_resolved(self):
        """Test that the update profile URL resolves to the correct view."""
        url = reverse('users:update_profile')
        self.assertEqual(resolve(url).func, employee_update_view)

    def test_password_change_url_is_resolved(self):
        """Test that the password change URL resolves to the correct view."""
        url = reverse('users:password_change')
        self.assertEqual(resolve(url).func, password_change_view)

    def test_password_change_done_url_is_resolved(self):
        """Test that the password change done URL resolves to the correct view."""
        url = reverse('users:password_change_done')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_delete_account_url_is_resolved(self):
        """Test that the delete account URL resolves to the correct view."""
        url = reverse('users:delete_account')
        self.assertEqual(resolve(url).func, delete_employee_view)

    def test_electricians_list_url_is_resolved(self):
        """Test that the electricians list URL resolves to the correct view."""
        url = reverse('users:electricians_list')
        self.assertEqual(resolve(url).func, electricians_list_view)

    def test_employee_tasks_url_is_resolved(self):
        """Test that the employee tasks URL resolves to the correct view."""
        url = reverse('users:employee_tasks', args=[1])
        self.assertEqual(resolve(url).func, employee_tasks_view)


class UsersURLAccessTests(TestCase):

    def test_register_url_access(self):
        """Test that the register URL is accessible via GET."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_access(self):
        """Test that the login URL is accessible via GET."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_employee_profile_url_access(self):
        """Test that the employee profile URL is accessible via GET."""
        response = self.client.get(reverse('users:employee_profile', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_electricians_list_url_access(self):
        """Test that the electricians list URL is accessible via GET."""
        response = self.client.get(reverse('users:electricians_list'))
        self.assertEqual(response.status_code, 200)
