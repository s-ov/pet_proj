from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

CustomUser = get_user_model()

class UserProfileViewTests(TestCase):
    """
        Test cases for the user profile view.
    """

    def setUp(self):
        """
            Create a test user and log in.
        """
        self.user = CustomUser.objects.create_user(
                cell_number='+380501234567',
                password='password123',
            )
        self.client.login(cell_number='+380501234567', password='password123')
        self.profile_url = reverse('users:user_profile', kwargs={'user_id': 1})

    def test_user_profile_view_with_valid_user(self):
        """
            Test that the user profile view returns a 200 status code for a valid user.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertContains(response, self.user.cell_number)

    def test_user_profile_view_with_invalid_user(self):
        """
            Test that the user profile view raises a 404 for an invalid cell_number.
        """
        invalid_url = reverse('users:user_profile', kwargs={'user_id': 2})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)