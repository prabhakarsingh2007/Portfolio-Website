from django.test import TestCase
from .models import Profile, Skill, Experience, Education
from django.utils import timezone

class PortfolioModelsTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Test User",
            title="Software Developer",
            bio="A test biography"
        )
        self.skill = Skill.objects.create(
            name="Python",
            proficiency=90,
            category="backend"
        )
        self.experience = Experience.objects.create(
            company="Test Corp",
            role="Engineer",
            start_date=timezone.now().date(),
            description="Point A\nPoint B"
        )
        self.education = Education.objects.create(
            school="Test University",
            degree="B.S. in CS",
            start_date=timezone.now().date()
        )

    def test_model_str_representations(self):
        self.assertEqual(str(self.profile), "Test User")
        self.assertEqual(str(self.skill), "Python (90%)")
        self.assertEqual(str(self.experience), "Engineer at Test Corp")
        self.assertEqual(str(self.education), "B.S. in CS from Test University")

    def test_experience_description_splitting(self):
        points = self.experience.get_description_points()
        self.assertEqual(len(points), 2)
        self.assertEqual(points[0], "Point A")
        self.assertEqual(points[1], "Point B")
