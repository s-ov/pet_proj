from django.test import TestCase
from django.urls import reverse

from task.models import Task
from users.models import Employee

class UserTasksViewTest(TestCase):
    
    def setUp(self):
        """Create a data for testing"""
        self.user = Employee.objects.create_user(
            cell_number='+3801234567',
            first_name='John',
            last_name='Doe',
            password='password123'
        )
        
        self.other_user = Employee.objects.create_user(
            cell_number='+3807654321',
            first_name='Jane',
            last_name='Smith',
            password='password123'
        )
        
        self.task1 = Task.objects.create(
            doer=self.user,
            task_description="Test Task 1",
            status=Task.TaskStatus.IN_PROGRESS
        )
        self.task2 = Task.objects.create(
            doer=self.user,
            task_description="Test Task 2",
            status=Task.TaskStatus.PENDING
        )
        
        self.other_task = Task.objects.create(
            doer=self.other_user,
            task_description="Other User Task",
            status=Task.TaskStatus.COMPLETED
        )
        
    def test_user_tasks_view_success(self):
        """Test that the view returns the correct tasks for the user"""
        response = self.client.get(reverse('users:employee_tasks', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/employee_tasks.html')
        self.assertContains(response, "Test Task 1")
        self.assertContains(response, "Test Task 2")
        self.assertNotContains(response, "Other User Task")
        
    def test_user_tasks_view_user_not_found(self):
        """Test that the view returns a 404 when the user does not exist"""
        response = self.client.get(reverse('users:employee_tasks', args=[999]))
        self.assertEqual(response.status_code, 404)
