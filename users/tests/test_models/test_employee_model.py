from django.test import TestCase
from users.models import Employee

class EmployeeModelTest(TestCase):

    def setUp(self):
        """Set up the data for the tests."""
        self.employee_data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'role': Employee.Role.ELECTRICIAN,
            'admission_group': Employee.AdmissionGroup.GROUP_I
        }

    def test_employee_creation_with_default_values(self):
        """Test creating an Employee instance with default role and admission group."""
        employee = Employee.objects.create_user(
            cell_number=self.employee_data['cell_number'],
            first_name=self.employee_data['first_name'],
            last_name=self.employee_data['last_name'],
            password=self.employee_data['password']
        )
        self.assertEqual(employee.role, Employee.Role.ELECTRICIAN)
        self.assertEqual(employee.admission_group, Employee.AdmissionGroup.NONE)
        self.assertEqual(Employee.objects.count(), 1)

    def test_employee_creation_with_custom_role_and_admission_group(self):
        """Test creating an Employee instance with custom role and admission group."""
        employee = Employee.objects.create_user(
            cell_number=self.employee_data['cell_number'],
            first_name=self.employee_data['first_name'],
            last_name=self.employee_data['last_name'],
            password=self.employee_data['password'],
            role=self.employee_data['role'],
            admission_group=self.employee_data['admission_group']
        )
        self.assertEqual(employee.role, Employee.Role.ELECTRICIAN)
        self.assertEqual(employee.admission_group, Employee.AdmissionGroup.GROUP_I)

    def test_employee_str_representation(self):
        """Test the string representation of an Employee."""
        employee = Employee.objects.create_user(**self.employee_data)
        expected_str = f"{employee.get_role_display()} - {employee.first_name} {employee.last_name}"
        self.assertEqual(str(employee), expected_str)

    def test_employee_role_choices(self):
        """Test that valid role choices can be assigned."""
        employee = Employee.objects.create_user(
            cell_number=self.employee_data['cell_number'],
            first_name=self.employee_data['first_name'],
            last_name=self.employee_data['last_name'],
            password=self.employee_data['password'],
            role=Employee.Role.ENGINEER
        )
        self.assertEqual(employee.role, Employee.Role.ENGINEER)
        self.assertEqual(employee.get_role_display(), 'Інженер')

    def test_employee_admission_group_choices(self):
        """Test that valid admission group choices can be assigned."""
        employee = Employee.objects.create_user(
            cell_number=self.employee_data['cell_number'],
            first_name=self.employee_data['first_name'],
            last_name=self.employee_data['last_name'],
            password=self.employee_data['password'],
            admission_group=Employee.AdmissionGroup.GROUP_III
        )
        self.assertEqual(employee.admission_group, Employee.AdmissionGroup.GROUP_III)
        self.assertEqual(employee.admission_group, 'ІII-тя група з електробезпеки')
