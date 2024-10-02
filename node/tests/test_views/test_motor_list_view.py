from django.test import TestCase
from django.urls import reverse
from node.models import NodeMotor
from django.core.paginator import Paginator

class MotorsListViewTest(TestCase):
    def setUp(self):
        """
        Set up some test data for the motors_list_view.
        """
        NodeMotor.objects.create(power=10.5, round_per_minute=1500, connection="▲", amperage=15)
        NodeMotor.objects.create(power=20, round_per_minute=1000, connection="✳", amperage=20)

    def test_motors_list_view_success(self):
        """
        Test that the motors_list_view returns a 200 status and displays the paginated motors list.
        """
        response = self.client.get(reverse('node:motors_list')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'node/motors_list.html')
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_motors_list_view_pagination(self):
        """
        Test pagination functionality.
        """
        NodeMotor.objects.create(power=30, round_per_minute=800, connection="▲", amperage=30)
        NodeMotor.objects.create(power=40, round_per_minute=500, connection="✳", amperage=40)

        response = self.client.get(reverse('node:motors_list'), {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

        response = self.client.get(reverse('node:motors_list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_motors_list_view_empty_page(self):
        """
        Test that an invalid page number returns the first page.
        """
        response = self.client.get(reverse('node:motors_list'), {'page': 999})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_motors_list_view_no_motors(self):
        """
        Test behavior when no motors exist in the database.
        """
        NodeMotor.objects.all().delete()  
        response = self.client.get(reverse('node:motors_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Двигунів немає.")
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_motors_list_view_page_not_an_integer(self):
        """
        Test that a non-integer page value defaults to the first page.
        """
        response = self.client.get(reverse('node:motors_list'), {'page': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_motors_list_view_handles_exceptions(self):
        """
        Test that exceptions are handled gracefully.
        """
        with self.assertRaises(NodeMotor.DoesNotExist):
            NodeMotor.objects.get(id=9999)
