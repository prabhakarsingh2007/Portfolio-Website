from django.test import TestCase
from django.urls import reverse

class CoreViewsTestCase(TestCase):
    def test_home_page_status(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_status(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_robots_txt_status_and_mime(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('User-agent:', response.content.decode())

    def test_sitemap_xml_status_and_mime(self):
        response = self.client.get(reverse('sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertIn('<urlset', response.content.decode())

    def test_service_worker_status_and_mime(self):
        response = self.client.get(reverse('service_worker'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/javascript')
        self.assertIn('antigravity-portfolio-v1', response.content.decode())
