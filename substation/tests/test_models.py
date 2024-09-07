from django.test import TestCase
from substation.models import Substation
from work_tower.models import WorkTowerLevel  

class SubstationModelTests(TestCase):
    def setUp(self):
        """Create a WorkTowerLevel instance for use in tests"""
        self.work_tower_level = WorkTowerLevel.objects.create(level='1')  

    def test_substation_creation(self):
        """
        Test that a Substation instance can be created with valid data.
        """
        substation = Substation.objects.create(
            title='РП-4',
            slug='rp-4',
            level=self.work_tower_level
        )
        self.assertEqual(substation.title, 'РП-4')
        self.assertEqual(substation.slug, 'rp-4')
        self.assertEqual(substation.level, self.work_tower_level)

    def test_title_choices(self):
        """
        Test that the title choices are correctly set.
        """
        valid_titles = dict(Substation.SUBSTATION_TITLES)
        for choice in valid_titles:
            substation = Substation(title=choice, slug='some-slug')
            self.assertIn(substation.title, valid_titles)

    def test_unique_slug(self):
        """
        Test that slug field is unique.
        """
        Substation.objects.create(
            title='РП-4',
            slug='unique-slug',
            level=self.work_tower_level
        )
        with self.assertRaises(Exception):
            Substation.objects.create(
                title='РП-5',
                slug='unique-slug',
                level=self.work_tower_level
            )

    def test_foreign_key_relationship(self):
        """
        Test the ForeignKey relationship to WorkTowerLevel.
        """
        substation = Substation.objects.create(
            title='РП-4',
            slug='substation-4',
            level=self.work_tower_level
        )
        self.assertEqual(substation.level, self.work_tower_level)

