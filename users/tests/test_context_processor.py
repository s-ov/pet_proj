from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.context_processors import user_info

from users.models import CustomUser

class UserInfoContextProcessorTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            cell_number='+380501234567',
            password='testpassword123',
        )

    def test_user_info_authenticated(self):
        """Test that user info is added to the context if the user is authenticated."""
        request = self.factory.get('/')
        request.user = self.user

        context = user_info(request)

        self.assertIn('user_profile_url', context)
        self.assertIn('home_url', context)
        self.assertIn('user_register_url', context)
        self.assertIn('user_login_url', context)
        self.assertIn('user_logout_url', context)
        self.assertIn('user_info', context)

        self.assertEqual(context['user_profile_url'], reverse('users:user_profile', kwargs={'user_id': self.user.id}))
        self.assertEqual(context['home_url'], reverse('users:home'))
        self.assertEqual(context['user_register_url'], reverse('users:register'))
        self.assertEqual(context['user_login_url'], reverse('users:login'))
        self.assertEqual(context['user_logout_url'], reverse('users:logout'))
        self.assertEqual(context['user_info'], self.user)

    def test_user_info_unauthenticated(self):
        # Simulate a request with an unauthenticated user
        request = self.factory.get('/')
        request.user = CustomUser()  # Anonymous user

        context = user_info(request)

        self.assertNotIn('user_profile_url', context)
        self.assertNotIn('home_url', context)
        self.assertNotIn('user_register_url', context)
        self.assertNotIn('user_login_url', context)
        self.assertNotIn('user_logout_url', context)
        self.assertNotIn('user_info', context)
