from django.test import TestCase
from django import forms
from users.employee_forms import EmployeeRegistrationForm
from users.models import CustomUser

class UserRegistrationFormTest(TestCase):
    """ Tests for UserRegistrationForm """

    def test_form_valid_data(self):
        """
            Test UserRegistrationForm with valid data: all fields should be valid
        """
        data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'admission_group': 'І-ша група з електробезпеки',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
        }
        form = EmployeeRegistrationForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_data(self):
        """ Test UserRegistrationForm with invalid data: all fields should be invalid """
        data = {
            'cell_number': '',
            'first_name': '',
            'last_name': '',
            'admission_group': 'Не вибрано',
            'password': '',
            'confirm_password': '',
        }
        form = EmployeeRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cell_number', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('confirm_password', form.errors)

    def test_passwords_mismatch(self):
        """ Test UserRegistrationForm with mismatched passwords """
        data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'admission_group': 'Group1',
            'password': 'securepassword',
            'confirm_password': 'differentpassword',
        }
        form = EmployeeRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Паролі не співпадають.'])

    def test_custom_error_messages(self):
        """ Test custom error messages """
        form = EmployeeRegistrationForm(data={})
        form.is_valid()  
        self.assertEqual(form.errors['cell_number'], ['Номер мобільного обов’язково.'])
        self.assertEqual(form.errors['password'], ['Пароль обов’язковий.'])

    def test_form_widgets_and_labels(self):
        """ Test form widgets and labels """
        form = EmployeeRegistrationForm()
        self.assertEqual(form.fields['cell_number'].widget.attrs['placeholder'], '+380501234567')
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'Ім\'я')
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Прізвище')
        self.assertEqual(form.fields['admission_group'].widget.attrs['placeholder'], 'Група допуску')

    def test_field_classes(self):
        form = EmployeeRegistrationForm()
        self.assertEqual(form.fields['cell_number'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['first_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['last_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['admission_group'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['confirm_password'].widget.attrs['class'], 'form-control')
