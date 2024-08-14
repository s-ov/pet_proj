from django.test import TestCase
from django import forms
from users.forms import UserLoginForm

class UserLoginFormTest(TestCase):
    """ Test the UserLoginForm class. """

    def test_form_initialization(self):
        """ Test that the form is initialized correctly. """
        form = UserLoginForm()
        self.assertIsInstance(form, forms.Form)
        self.assertIn('cell_number', form.fields)
        self.assertIn('password', form.fields)
    
    def test_field_attributes(self):
        """ Test that the field attributes are set correctly. """
        form = UserLoginForm()
        
        cell_number_field = form.fields['cell_number']
        self.assertEqual(cell_number_field.widget.attrs['class'], 'form-control')
        self.assertEqual(cell_number_field.widget.attrs['placeholder'], '+380501234567')
        
        password_field = form.fields['password']
        self.assertEqual(password_field.widget.attrs['class'], 'form-control')
        self.assertEqual(password_field.widget.attrs['placeholder'], 'Введіть Ваш пароль')

    def test_form_valid_data(self):
        """ Test UserLoginForm with valid data """
        form_data = {'cell_number': '+380501234567', 'password': 'securepassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_data_missing_cell_number(self):
        """ Test UserLoginForm with invalid data: cell_number is missing """
        form_data = {'password': 'securepassword'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cell_number', form.errors)
    
    def test_form_invalid_data_missing_password(self):
        """ Test UserLoginForm with invalid data: password is missing """
        form_data = {'cell_number': '+380501234567'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
    
    def test_form_invalid_data_long_cell_number(self):
        """ Test UserLoginForm with invalid data: cell_number is too long """
        form_data = {'cell_number': '+3805012378901234567890', 'password': 'securepassword'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cell_number', form.errors)

    def test_form_invalid_data_long_password(self):
        """ Test UserLoginForm with invalid data: password is too long """
        form_data = {'cell_number': '+380501234567', 'password': 'a' * 51}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

