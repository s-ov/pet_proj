from django.test import TestCase
from django import forms
from users.models import Employee
from users.employee_forms import EmployeeCellUpdateForm


class UserCellUpdateFormTest(TestCase):
    """ Test the UserCellUpdateForm class. """
    
    def setUp(self):
        """ Set up a CustomUser instance for testing. """
        self.user = Employee.objects.create_user(
            cell_number='1234567890',
            password='password123',
            
        )

    def test_form_initialization(self):
        """ Test form is initialized with the correct instance data """
        form = EmployeeCellUpdateForm(instance=self.user)
        self.assertEqual(form.instance, self.user)
        self.assertEqual(form.initial['cell_number'], self.user.cell_number)
    
    def test_form_fields(self):
        """ Test that the form has the correct fields. """
        form = EmployeeCellUpdateForm()

        self.assertIn('cell_number', form.fields)
        self.assertIn('password', form.fields)

        self.assertEqual(form.fields['cell_number'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Введіть Ваш пароль')

    def test_form_valid_data(self):
        """ Test the form with valid data """
        form_data = {
            'cell_number': '+380987654321',  
            'password': 'password123'
        }
        form = EmployeeCellUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.cell_number, '+380987654321')    

    def test_form_invalid_data(self):
        """ Test the form with invalid data. """
        form_data = {
            'cell_number': '',
            'password': 'password123'
        }
        form = EmployeeCellUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('cell_number', form.errors)
        
    def test_form_rendering(self):
        """ Test that the form renders correctly. """
        form = EmployeeCellUpdateForm()
        rendered_form = form.as_p()  
        self.assertIn('<input type="password" name="password"', rendered_form)
        self.assertIn('<input type="text" name="cell_number"', rendered_form)
        self.assertIn('Введіть Ваш пароль', rendered_form)
        self.assertIn('Номер мобільного', rendered_form)
