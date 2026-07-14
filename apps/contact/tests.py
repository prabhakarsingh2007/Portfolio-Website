from django.test import TestCase
from django.urls import reverse
from .models import ContactMessage

class ContactTestCase(TestCase):
    def test_contact_page_get(self):
        response = self.client.get(reverse('contact:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Send a Message")

    def test_contact_form_submission_success(self):
        post_data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'subject': 'Inquiry',
            'message': 'Looking for a Django Developer.'
        }
        response = self.client.post(reverse('contact:index'), post_data)
        # Check standard redirect response
        self.assertEqual(response.status_code, 302)
        # Verify db persistence
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().name, 'Alice Smith')

    def test_contact_ajax_form_submission_success(self):
        post_data = {
            'name': 'Bob Johnson',
            'email': 'bob@example.com',
            'subject': 'Freelance project',
            'message': 'Need support with docker routing.',
            'ajax': 'true'
        }
        # Simulate ajax header in request
        response = self.client.post(
            reverse('contact:index'),
            post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertIn('sent successfully', json_data['message'])

    def test_contact_ajax_form_submission_invalid(self):
        post_data = {
            'name': 'Bob Johnson',
            'email': 'not-an-email', # Invalid
            'subject': '',
            'message': 'No content.',
            'ajax': 'true'
        }
        response = self.client.post(
            reverse('contact:index'),
            post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data['success'])
        self.assertIn('errors', json_data)
