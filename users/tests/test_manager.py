from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class CustomUserManagerTest(TestCase):

    def test_create_user_with_cell_number(self):
        """Test that a user is created with a cell number."""
        cell_number = '+380501234567'
        password = 'testpassword123'
        user = CustomUser.objects.create_user(cell_number=cell_number, password=password)
        
        self.assertEqual(user.cell_number, cell_number)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_cell_number(self):
        """Test that creating a user without a cell number raises an error."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(cell_number=None, password='testpassword123')

    def test_create_superuser(self):
        """Test that a superuser is created with a cell number."""
        cell_number = '+380501234567'
        password = 'superpassword123'
        user = CustomUser.objects.create_superuser(cell_number=cell_number, password=password)
        
        self.assertEqual(user.cell_number, cell_number)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_with_invalid_permissions(self):
        """Test that a superuser must have is_staff and is_superuser set to True."""
        cell_number = '+380501234567'
        password = 'superpassword123'
        
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                cell_number=cell_number, 
                password=password, 
                is_staff=False
            )
        
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                cell_number=cell_number, 
                password=password, 
                is_superuser=False
            )
