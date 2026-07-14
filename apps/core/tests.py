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

from apps.portfolio.models import Profile, Skill, Experience, Education, Certificate, Testimonial
from apps.projects.models import Project
from apps.blog.models import Post, Category
from django.contrib.auth.models import User
from django.utils import timezone

class CoreAPIsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('author', 'author@example.com', 'pwd123')
        self.profile = Profile.objects.create(
            name="Alexander Wright",
            title="Lead Engineer",
            bio="My bio",
            email="alex@example.com"
        )
        self.skill = Skill.objects.create(name="Python", proficiency=90, category="backend")
        self.experience = Experience.objects.create(
            company="NexTech",
            role="Engineer",
            start_date=timezone.now().date(),
            description="My role description"
        )
        self.education = Education.objects.create(
            school="UC Berkeley",
            degree="M.S.",
            start_date=timezone.now().date()
        )
        self.project = Project.objects.create(
            title="SaaS API",
            summary="A short summary",
            description="Detailed body",
            technologies="Django, Postgres"
        )
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Django 6 Features",
            summary="A short summary",
            body="Body text",
            author=self.user,
            category=self.category,
            status='published'
        )
        self.certificate = Certificate.objects.create(
            name="AWS SA",
            issuing_organization="AWS",
            issue_date=timezone.now().date()
        )
        self.testimonial = Testimonial.objects.create(
            client_name="Sarah",
            client_title="Director",
            quote="Great developer!"
        )

    def test_profile_api(self):
        response = self.client.get(reverse('api:profile'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "Alexander Wright")
        self.assertEqual(data['socials']['github'], "")

    def test_skills_api(self):
        response = self.client.get(reverse('api:skills'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['skills']), 1)
        self.assertEqual(data['skills'][0]['name'], "Python")

    def test_experience_api(self):
        response = self.client.get(reverse('api:experience'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['experiences']), 1)
        self.assertEqual(data['experiences'][0]['company'], "NexTech")

    def test_education_api(self):
        response = self.client.get(reverse('api:education'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['education']), 1)
        self.assertEqual(data['education'][0]['school'], "UC Berkeley")

    def test_projects_api(self):
        response = self.client.get(reverse('api:projects'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['projects']), 1)
        self.assertEqual(data['projects'][0]['title'], "SaaS API")

    def test_project_detail_api(self):
        response = self.client.get(reverse('api:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "SaaS API")

    def test_blog_api(self):
        response = self.client.get(reverse('api:blog'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['posts']), 1)

    def test_blog_detail_api(self):
        response = self.client.get(reverse('api:blog_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Django 6 Features")

    def test_certificates_api(self):
        response = self.client.get(reverse('api:certificates'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['certificates']), 1)

    def test_testimonials_api(self):
        response = self.client.get(reverse('api:testimonials'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['testimonials']), 1)

    def test_contact_submit_api_success(self):
        payload = {
            'name': 'Test User',
            'email': 'user@example.com',
            'subject': 'Hello',
            'message': 'Hi Alexander!'
        }
        response = self.client.post(reverse('api:contact'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_contact_submit_api_failure(self):
        payload = {
            'name': '',
            'email': 'invalid-email',
            'subject': 'Hello',
            'message': ''
        }
        response = self.client.post(reverse('api:contact'), payload)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
