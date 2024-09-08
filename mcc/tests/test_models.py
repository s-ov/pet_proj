from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from mcc.models import MotorControlCenter
from substation.models import Substation

class MotorControlCenterModelTests(TestCase):

    def setUp(self):
        """Setup a substation instance to be used in tests"""
        self.substation = Substation.objects.create(title="Test Substation")
    
    def test_motor_control_center_creation(self):
        """Test that a MotorControlCenter instance is created successfully."""
        mcc = MotorControlCenter.objects.create(
            title='MCC-1',
            slug='mcc-1',
            substation=self.substation
        )
        self.assertEqual(mcc.title, 'MCC-1')
        self.assertEqual(mcc.slug, 'mcc-1')
        self.assertEqual(mcc.substation, self.substation)

    def test_motor_control_center_slug_uniqueness(self):
        """Test that the slug field is unique."""
        MotorControlCenter.objects.create(
            title='MCC-1',
            slug='mcc-unique',
            substation=self.substation
        )
        with self.assertRaises(IntegrityError):
            MotorControlCenter.objects.create(
                title='MCC-2',
                slug='mcc-unique',
                substation=self.substation
            )

    def test_motor_control_center_default_values(self):
        """Test that default values are properly set."""
        mcc = MotorControlCenter.objects.create(
            title='MCC-3',
            slug='mcc-3'
        )
        self.assertEqual(mcc.title, 'MCC-3')
        self.assertEqual(mcc.slug, 'mcc-3')
        self.assertIsNone(mcc.substation)

    def test_motor_control_center_related_name(self):
        """Test the related name for the ForeignKey."""
        mcc = MotorControlCenter.objects.create(
            title='MCC-5',
            slug='mcc-5',
            substation=self.substation
        )
        related_mccs = self.substation.mccs.all()
        self.assertIn(mcc, related_mccs)
