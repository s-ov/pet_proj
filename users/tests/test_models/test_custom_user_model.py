from django.test import TestCase
from users.models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserModelTest(TestCase):

    def setUp(self):
        """Set up the data for the tests."""
        self.user_data = {
            'cell_number': '+380501234567',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
        }

    def test_customuser_creation(self):
        """Test that a CustomUser instance can be created successfully."""
        user = CustomUser.objects.create_user(
            cell_number=self.user_data['cell_number'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            password=self.user_data['password']
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(user.cell_number, self.user_data['cell_number'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])

    def test_customuser_duplicate_cell_number(self):
        """Test that CustomUser enforces unique constraint on cell_number."""
        CustomUser.objects.create_user(**self.user_data)
        with self.assertRaises(ValidationError):
            duplicate_user = CustomUser(
                cell_number=self.user_data['cell_number'],
                first_name="Jane",
                last_name="Smith",
            )
            duplicate_user.full_clean()

    def test_customuser_invalid_cell_number(self):
        """Test that CustomUser enforces valid cell_number format."""
        invalid_cell_number = '+123456789'
        user = CustomUser(
            cell_number=invalid_cell_number,
            first_name="Invalid",
            last_name="User",
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  

    def test_customuser_str_representation(self):
        """Test the string representation of CustomUser."""
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), f"{user.first_name} {user.last_name}")
