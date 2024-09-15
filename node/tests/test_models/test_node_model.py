from django.core.exceptions import ValidationError
from django.test import TestCase

from node.models import Node, NodeMotor
from work_tower.models import WorkTowerLevel
from mcc.models import MotorControlCenter

class NodeModelTest(TestCase):

    def setUp(self):
        """Set up initial data for tests"""
        self.work_tower_level = WorkTowerLevel.objects.create(level="1")
        self.node_motor = NodeMotor.objects.create(
            power=100.00,
            round_per_minute=3000,
            connection='✳',
            amperage=10.00
        )
        self.mcc = MotorControlCenter.objects.create(title="MCC 1")

    def test_node_creation(self):
        """Test that a Node instance can be created with valid data"""
        node = Node.objects.create(
            name='Засувка',
            index='Node1',
            level=self.work_tower_level,
            motor=self.node_motor,
            mcc=self.mcc
        )
        self.assertEqual(node.name, 'Засувка')
        self.assertEqual(node.index, 'Node1')
        self.assertEqual(node.level, self.work_tower_level)
        self.assertEqual(node.motor, self.node_motor)
        self.assertEqual(node.mcc, self.mcc)

    def test_unique_index(self):
        """Test that the index field is unique"""
        Node.objects.create(
            name='Клапан 3-х ходовий',
            index='Node2',
            level=self.work_tower_level,
            motor=self.node_motor,
            mcc=self.mcc
        )
        with self.assertRaises(ValidationError):
            node_with_duplicate_index = Node(
                name='Вентилятор',
                index='Node2',  
                level=self.work_tower_level,
                motor=self.node_motor,
                mcc=self.mcc
            )
            node_with_duplicate_index.full_clean()  

    def test_node_type_choices(self):
        """Test that the name field adheres to choices"""
        valid_names = [choice[0] for choice in Node.NODE_TYPES]
        for name in valid_names:
            node = Node(
                name=name,
                index=f'{name}_UniqueIndex',
                level=self.work_tower_level,
                motor=self.node_motor,
                mcc=self.mcc
            )
            try:
                node.full_clean()  
            except ValidationError:
                self.fail(f"ValidationError raised for valid choice {name}")
        
        node = Node(
            name='InvalidType',
            index='UniqueIndex2',
            level=self.work_tower_level,
            motor=self.node_motor,
            mcc=self.mcc
        )
        with self.assertRaises(ValidationError):
            node.full_clean()  

    def test_relationships(self):
        """Test foreign key relationships"""
        node = Node.objects.create(
            name='Шнек зачисний',
            index='Node3',
            level=self.work_tower_level,
            motor=self.node_motor,
            mcc=self.mcc
        )
        self.assertEqual(node.level, self.work_tower_level)
        self.assertEqual(node.motor, self.node_motor)
        self.assertEqual(node.mcc, self.mcc)
