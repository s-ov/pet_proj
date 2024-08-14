from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordChangeDoneView

from users.views import (
                        index_view, 
                        users_view, 
                        user_register_view, 
                        user_login_view, 
                        user_profile_view, 
                        user_update_view, 
                        password_change_view, 
                        user_logout_view, 
                        delete_user_view,
                        )

class UsersURLsTest(SimpleTestCase):

    def test_home_url(self):
        """
            Tests that the 'users:home' URL resolves to the index_view function.
        """
        url = reverse('users:home')
        self.assertEqual(resolve(url).func, index_view)

    def test_users_url(self):
        """
            Tests that the 'users:users' URL resolves to the users_view function.
        """
        url = reverse('users:users')
        self.assertEqual(resolve(url).func, users_view)

    def test_register_url(self):
        """
            Tests that the 'users:register' URL resolves to the user_register_view function.
        """
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, user_register_view)

    def test_login_url(self):
        """
            Tests that the 'users:login' URL resolves to the user_login_view function.
        """
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, user_login_view)

    def test_logout_url(self):
        """
            Tests that the 'users:logout' URL resolves to the user_logout_view function.
        """
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, user_logout_view)

    def test_user_profile_url(self):
        """
            Tests that the 'users:user_profile' URL resolves to the user_profile_view function.
        """
        url = reverse('users:user_profile', args=[1])
        self.assertEqual(resolve(url).func, user_profile_view)

    def test_update_profile_url(self):
        """
            Tests that the 'users:update_profile' URL resolves to the user_update_view function.
        """
        url = reverse('users:update_profile')
        self.assertEqual(resolve(url).func, user_update_view)

    def test_password_change_url(self):
        """
            Tests that the 'users:change_password' URL resolves to the password_change_view function.
        """
        url = reverse('users:password_change')
        self.assertEqual(resolve(url).func, password_change_view)

    def test_password_change_done_url(self):
        """
            Tests that the 'users:password_change_done' works correctly.
        """
        url = reverse('users:password_change_done')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeDoneView)

    def test_delete_account_url(self):
        """
            Tests that the 'users:delete_account' URL resolves to the delete_user_view function.
        """
        url = reverse('users:delete_account')
        self.assertEqual(resolve(url).func, delete_user_view)
