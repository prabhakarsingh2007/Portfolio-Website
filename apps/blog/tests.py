from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post, Category

class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('author', 'author@example.com', 'pwd123')
        self.category = Category.objects.create(name="Tech Tutorials")
        
        # Post 1 (Published)
        self.post = Post.objects.create(
            title="Django Query Optimizations",
            summary="A guide on select_related and prefetch_related.",
            body="Word " * 250, # 250 words -> should be roughly 1 min read time
            author=self.user,
            category=self.category,
            status='published',
            published_date=timezone.now()
        )
        
        # Post 2 (Draft)
        self.draft_post = Post.objects.create(
            title="Kubernetes Basics",
            summary="Intro to pods.",
            body="Word " * 10,
            author=self.user,
            category=self.category,
            status='draft'
        )

    def test_reading_time_estimation(self):
        # 250 words / 200 = 1.25 -> rounded to 1 min
        self.assertEqual(self.post.reading_time, 1)

    def test_view_counter_increment(self):
        initial_views = self.post.views
        response = self.client.get(reverse('blog:detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)

    def test_draft_posts_hidden_from_list(self):
        response = self.client.get(reverse('blog:list'))
        self.assertContains(response, "Django Query Optimizations")
        self.assertNotContains(response, "Kubernetes Basics")

    def test_draft_posts_hidden_from_detail(self):
        response = self.client.get(reverse('blog:detail', kwargs={'slug': self.draft_post.slug}))
        self.assertEqual(response.status_code, 404)

    def test_blog_search(self):
        response = self.client.get(reverse('blog:list'), {'q': 'Optimizations'})
        self.assertIn(self.post, response.context['posts'])
        
        response = self.client.get(reverse('blog:list'), {'q': 'NonExistentWord'})
        self.assertNotIn(self.post, response.context['posts'])

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('blog:detail', kwargs={'slug': self.post.slug}))
