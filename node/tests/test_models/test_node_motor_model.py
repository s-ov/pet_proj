from django.test import TestCase
from django.core.exceptions import ValidationError
from node.models import NodeMotor

class NodeMotorModelTest(TestCase):
    
    def test_node_motor_creation(self):
        """Test that a NodeMotor instance can be created"""
        node_motor = NodeMotor.objects.create(
            power=150.00,
            round_per_minute=4000,
            connection='▲',
            amperage=12.00
        )
        self.assertEqual(node_motor.power, 150.00)
        self.assertEqual(node_motor.round_per_minute, 4000)
        self.assertEqual(node_motor.connection, '▲')
        self.assertEqual(node_motor.amperage, 12.00)

    def test_default_values(self):
        """Test that default values are set correctly"""
        node_motor = NodeMotor.objects.create()
        self.assertEqual(node_motor.power, 0.00)
        self.assertEqual(node_motor.round_per_minute, 0)
        self.assertEqual(node_motor.connection, '▲')
        self.assertEqual(node_motor.amperage, 0.00)

    def test_choices_field(self):
        """Test that the connection field has correct choices"""
        valid_choices = [choice[0] for choice in NodeMotor.SYMBOL_CHOICES]
        for choice in valid_choices:
            node_motor = NodeMotor.objects.create(
                power=50.00,
                round_per_minute=1000,
                connection=choice,
                amperage=5.00
            )
            self.assertIn(node_motor.connection, valid_choices)
        