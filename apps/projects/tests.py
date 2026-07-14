from django.test import TestCase
from django.urls import reverse
from .models import Project

class ProjectsTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="E-Commerce API",
            summary="A short summary",
            description="Detailed markdown text case study",
            technologies="Django, Postgres, Docker",
            is_featured=True
        )

    def test_project_slug_auto_generation(self):
        self.assertEqual(self.project.slug, "e-commerce-api")

    def test_project_tech_list_splitting(self):
        tech_list = self.project.get_tech_list()
        self.assertEqual(len(tech_list), 3)
        self.assertIn("Django", tech_list)
        self.assertIn("Postgres", tech_list)

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "E-Commerce API")
        self.assertContains(response, "Django")

    def test_project_detail_view(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detailed markdown text case study")

    def test_get_absolute_url(self):
        self.assertEqual(self.project.get_absolute_url(), reverse('projects:detail', kwargs={'slug': self.project.slug}))
