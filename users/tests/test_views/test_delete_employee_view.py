from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

class DeleteUserViewTest(TestCase):

    def setUp(self):
        """ 
            Set up a user instance for testing. 
        """
        self.user = get_user_model().objects.create_user(
            cell_number='+380501234567',
            password='correct_password'
        )
        self.client.login(cell_number='+380501234567', password='correct_password')
        self.url = reverse('users:delete_account')
        

    def test_get_request(self):
        """
            Test that the delete form is rendered on GET request.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete_user.html')
        self.assertIn('form', response.context)
        self.assertContains(response, 'Введіть пароль')

    def test_post_request_with_correct_password(self):
        """
            Test that the user is deleted when the correct password is provided.
        """
        response = self.client.post(self.url, {'password': 'correct_password'})
        self.assertRedirects(response, reverse('users:login'))
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ваш обліковий запис було видалено.')

    def test_post_request_with_incorrect_password(self):
        """
            Test that the user is not deleted when the wrong password is provided.
        """
        response = self.client.post(self.url, {'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete_user.html')
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertFormError(response, 'form', 'password', "Невірний пароль. Будь ласка, спробуйте ще раз.")

    def test_post_request_without_password(self):
        """
            Test that the user is not deleted when no password is provided.
        """
        response = self.client.post(self.url, {'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete_user.html')
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertFormError(response, 'form', 'password', "Це поле обов'язкове.")
