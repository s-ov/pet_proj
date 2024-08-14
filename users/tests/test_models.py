from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import CustomUser

class CustomUserModelTests(TestCase):
    def setUp(self):
        """
            Create a user instance for use in tests.
        """
        self.user = CustomUser.objects.create(
            cell_number='+380501234567',
            first_name='John',
            last_name='Doe',
            role='Electrician',
            admission_group='I'
        )

    def test_user_creation(self):
        """
            Test the creation of a CustomUser instance.
        """
        self.assertEqual(self.user.cell_number, '+380501234567')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.role, 'Electrician')
        self.assertEqual(self.user.admission_group, 'I')
    
    def test_invalid_cell_number(self):
        """
            Test that invalid cell numbers raise a ValidationError.
        """
        invalid_numbers = [
            '+380123456789',    # Invalid prefix
            '+38050123456',     # Too short
            '+3805012345678',   # Too long
            '+390501234567',    # Wrong country code
            '+38050123456a'     # Contains non-numeric characters
        ]
        
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                user = CustomUser(cell_number=number)
                user.full_clean()  

    def test_str_method(self):
        """
            Test the __str__ method of the CustomUser model.
        """
        self.assertEqual(str(self.user), '+380501234567')

    def test_role_choices(self):
        """Test that the role choices are set correctly."""
        valid_roles = dict(CustomUser.ROLES)
        self.assertIn(self.user.role, valid_roles)

    def test_admission_group_choices(self):
        """
            Test that the admission group choices are set correctly.
        """
        valid_groups = dict(CustomUser.ADMISSION_GROUP).values()
        self.assertIn(self.user.admission_group, valid_groups)

    def test_blank_admission_group(self):
        """
            Test that admission_group can be blank.
        """
        user_with_blank_admission_group = CustomUser.objects.create(
            cell_number='+380501234568',
            first_name='Jane',
            last_name='Doe',
            role='Ingineer',
            admission_group=''  
        )
        self.assertEqual(user_with_blank_admission_group.admission_group, '')

    def test_unique_cell_number(self):
        """
            Test wether the not unique cell_number raises exception.
        """
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                cell_number='+380501234567', 
                first_name='Duplicate',
                last_name='User',
                role='Electrician',
                admission_group='II'
            )
    
    def test_user_without_username(self):
        """
            Test that the username field is None.
        """
        self.assertIsNone(self.user.username)
