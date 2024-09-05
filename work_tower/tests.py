from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import WorkTowerLevel
from .admin import WorkTowerLevelAdmin


class WorkTowerLevelModelTest(TestCase):
    
    def test_create_valid_level(self):
        """Test creating instances with valid levels"""
        for value, display in WorkTowerLevel.LEVELS:
            level_instance = WorkTowerLevel.objects.create(level=value)
            self.assertEqual(level_instance.level, value)

    def test_create_invalid_level(self):
        """Test that an error is raised for invalid level values"""
        invalid_level = 999.9
        instance = WorkTowerLevel(level=invalid_level)
        with self.assertRaises(ValidationError):
            instance.clean()

    def test_default_value(self):
        """Test that the default value is 0.0"""
        default_instance = WorkTowerLevel.objects.create()
        self.assertEqual(default_instance.level, 0.0)

    def test_field_choices(self):
        """Test that the choices for the field are set correctly"""
        valid_choices = dict(WorkTowerLevel.LEVELS)
        for value, display in WorkTowerLevel.LEVELS:
            self.assertIn(value, valid_choices)
            self.assertEqual(valid_choices[value], display)
    
    def test_field_max_length(self):
        """Test that the max_length attribute is not being exceeded"""
        field = WorkTowerLevel._meta.get_field('level')
        self.assertEqual(field.max_length, 100)

    def test_str_representation(self):
        """Test that the __str__ method returns the expected output"""
        level_instance = WorkTowerLevel(level=4.8)
        self.assertEqual(str(level_instance), '4.8')

    def test_level_validation(self):
        """Test that only valid levels can be saved"""
        valid_levels = [level for level, display in WorkTowerLevel.LEVELS]
        for level in valid_levels:
            instance = WorkTowerLevel(level=level)
            instance.full_clean()  
            instance.save()
        invalid_level = 100.0
        instance = WorkTowerLevel(level=invalid_level)
        with self.assertRaises(ValidationError):
            instance.full_clean()  


class WorkTowerAreasAdminTest(TestCase):

    def setUp(self):
        """Create test data for the admin view"""
        self.level = WorkTowerLevel.objects.create(level=4.8)
        self.admin_site = site

    def test_admin_registration(self):
        """Ensure WorkTowerLevel is registered with the admin site"""
        self.assertIsInstance(self.admin_site._registry[WorkTowerLevel], WorkTowerLevelAdmin)

    def test_list_display(self):
        """ Ensure list_display contains the 'level' field"""
        admin_instance = self.admin_site._registry[WorkTowerLevel]
        self.assertEqual(list(admin_instance.list_display), ['level'])
