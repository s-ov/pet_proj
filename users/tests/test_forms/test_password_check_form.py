from django.test import TestCase
from django.contrib.auth import get_user_model
from users.employee_forms import EmployeePasswordCheckForm

class UserPasswordCheckFormTest(TestCase):

    def setUp(self):
        """ 
            Set up a CustomUser instance for testing. 
        """
        self.user = get_user_model().objects.create_user(
            cell_number='+380501234567',
            password='correct_password'
        )

    def test_form_valid_with_correct_password(self):
        """ 
            Test form with valid data: password is correct 
        """
        form_data = {'password': 'correct_password'}
        form = EmployeePasswordCheckForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_incorrect_password(self):
        """ 
            Test form with invalid data: password is incorrect 
        """
        form_data = {'password': 'wrong_password'}
        form = EmployeePasswordCheckForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'], ["Невірний пароль. Будь ласка, спробуйте ще раз."])

    def test_empty_password(self):
        """ 
            Test form with empty password 
        """
        form_data = {'password': ''}
        form = EmployeePasswordCheckForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_form_initialization(self):
        """ 
            Test that the form is initialized correctly with the user 
        """
        form = EmployeePasswordCheckForm(user=self.user)
        self.assertEqual(form.user, self.user)

    def test_form_widget_attributes(self):
        """
            Test that the form widget attributes are set correctly
        """
        form = EmployeePasswordCheckForm(user=self.user)
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Введіть пароль')
