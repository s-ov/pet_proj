from django.test import TestCase
from django.contrib.auth import get_user_model
from django import forms
from users.employee_forms import EmployeePasswordChangeForm  


class UserPasswordChangeFormTests(TestCase):
    """ Test the UserPasswordChangeForm """

    def setUp(self):
        """ Set up a CustomUser instance for testing. """
        self.user = get_user_model().objects.create_user(
            cell_number='+380987654321',
            password='old_password'
        )
        self.user.save()

    def test_form_valid_data(self):
        """ Test the form with valid data """
        form_data = {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        form = EmployeePasswordChangeForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_old_password_incorrect(self):
        """ Test old password is incorrect """
        form_data = {
            'old_password': 'wrong_password',
            'new_password1': 'new_password123',
            'new_password2': 'new_password123',
        }
        form = EmployeePasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)
        self.assertEqual(form.errors['old_password'], 
                         ['Старий пароль було введено неправильно. Будь ласка, введіть його знову.']
                         )

    def test_new_password_mismatch(self):
        """ Test new password is mismatch """
        form_data = {
            'old_password': 'old_password',
            'new_password1': 'new_password123',
            'new_password2': 'different_password123',
        }
        form = EmployeePasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)
        self.assertEqual(form.errors['new_password2'], ['Паролі не збігаються'])

    def test_new_password_required(self):
        """ Test new password is required """
        form_data = {
            'old_password': 'old_password',
            'new_password1': '',
            'new_password2': '',
        }
        form = EmployeePasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password1', form.errors)
        self.assertEqual(form.errors['new_password1'], ['Будь ласка, введіть новий пароль.'])
        self.assertIn('new_password2', form.errors)
        self.assertEqual(form.errors['new_password2'], ['Будь ласка, підтверджте новий пароль.'])

    def test_new_password_too_short(self):
        """ Test new password too short """
        
        form_data_short = {
            'old_password': 'old_password',
            'new_password1': '123',
            'new_password2': '123'
        }
        form_short = EmployeePasswordChangeForm(user=self.user, data=form_data_short)
        self.assertFalse(form_short.is_valid())
        self.assertIn('new_password1', form_short.errors)
        self.assertEqual(form_short.errors['new_password1'], ['Пароль занадто короткий: не менше 8 символів.'])

    def test_new_password_too_long(self):
        """ Test new password max length """
        long_password = 'a' * 129  
        form_data = {
            'old_password': 'old_password',
            'new_password1': long_password,
            'new_password2': long_password,
        }
        form = EmployeePasswordChangeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password1', form.errors)
        self.assertEqual(form.errors['new_password1'], ['Пароль занадто довгий: не більше 50 символів.'])

    def test_valid_length_password(self):
        """ Test valid length password """
        form_data_valid = {
            'old_password': 'old_password',
            'new_password1': 'validpassword123',
            'new_password2': 'validpassword123'
        }
        form_valid = EmployeePasswordChangeForm(user=self.user, data=form_data_valid)
        self.assertTrue(form_valid.is_valid())
