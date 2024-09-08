from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.template import TemplateDoesNotExist

from substation.models import Substation
from mcc.models import MotorControlCenter as MCC

class SubstationMCCsViewTests(TestCase):

    def setUp(self):
        """Create test data for the view tests."""
        self.substation = Substation.objects.create(slug='test-substation', title='Test Substation')
        
        self.mcc1 = MCC.objects.create(title='MCC-1', slug='mcc-1', substation=self.substation)
        self.mcc2 = MCC.objects.create(title='MCC-2', slug='mcc-2', substation=self.substation)
        
        self.url = reverse('mcc:substation_mccs', kwargs={'substation_slug': self.substation.slug})

    def test_substation_mccs_view_valid_substation(self):
        """Test that the view returns the correct context and template for a valid substation slug."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mcc/substation_mccs.html')
        self.assertIn('substation', response.context)
        self.assertIn('mccs', response.context)
        self.assertEqual(response.context['substation'], self.substation)
        self.assertIn(self.mcc1, response.context['mccs'])
        self.assertIn(self.mcc2, response.context['mccs'])

    def test_substation_mccs_view_invalid_substation(self):
        """Test that the view raises a 404 error for an invalid substation slug."""
        invalid_url = reverse('mcc:substation_mccs', kwargs={'substation_slug': 'invalid-slug'})
        
        response = self.client.get(invalid_url)
        
        self.assertEqual(response.status_code, 404) 
