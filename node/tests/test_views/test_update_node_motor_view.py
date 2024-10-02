from django.test import TestCase
from django.urls import reverse
from node.models import NodeMotor
from node.forms import NodeMotorCreationForm

class UpdateNodeMotorViewTests(TestCase):
    def setUp(self):
        """Create a sample NodeMotor instance for testing"""
        self.motor = NodeMotor.objects.create(power=10.0)  
        self.url = reverse('node:update_motor')

    def test_update_motor_with_valid_data(self):
        """Test update of NodeMotor with valid data"""
        response = self.client.post(self.url, {
        'motor_id': self.motor.id,
        'power': '15.0',
        'update': 'Update'  
        })
        
        self.assertEqual(response.status_code, 200)

        self.motor.refresh_from_db()
        self.assertEqual(self.motor.power, 10.0)

    def test_update_motor_with_invalid_power(self):
        """Test update with invalid power value"""
        response = self.client.post(self.url, {
            'motor_id': self.motor.id,
            'power': 'invalid_power',
            'update': 'Update'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не правильний ввід. Введіть, буль ласка, числове значення.')

    def test_update_motor_without_power(self):
        """Test update without providing power value"""
        response = self.client.post(self.url, {
            'motor_id': self.motor.id,
            'update': 'Update'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введіть, буль ласка, потужність.')

    
    def test_update_motor_not_found(self):
        """Test update with a non-existent motor"""
        response = self.client.post(self.url, {
        'motor_id': 9999,  
        'power': '15.0',
        'update': 'Update'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Двигун з ID 9999 не знайдено.')

    def test_get_update_motor_form(self):
        """Test GET request for the update form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/update_motor_form.html')

