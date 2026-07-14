import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from apps.portfolio.models import Profile, Skill, Experience, Education, Certificate, Testimonial
from apps.projects.models import Project
from apps.blog.models import Category, Post

# PIL helper to generate dummy image files in media
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class Command(BaseCommand):
    help = 'Pre-populates the database with premium mock portfolio and blog data'

    def handle(self, *args, **options):
        self.stdout.write('Starting data pre-population...')

        # 1. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created (password: adminpass123)'))
        else:
            self.stdout.write('Superuser "admin" already exists.')

        admin_user = User.objects.get(username='admin')

        # Create media sub-directories if they don't exist
        os.makedirs('media/profile', exist_ok=True)
        os.makedirs('media/projects', exist_ok=True)
        os.makedirs('media/blog', exist_ok=True)

        # Helper to generate dummy images
        def generate_dummy_image(filepath, text, color):
            if HAS_PIL:
                img = Image.new('RGB', (800, 500) if 'profile' not in filepath else (400, 400), color=color)
                draw = ImageDraw.Draw(img)
                # Draw simple text block center
                draw.rectangle([(20, 20), (img.width-20, img.height-20)], outline='#ffffff', width=2)
                draw.text((img.width/4, img.height/2.2), text, fill='#ffffff')
                img.save(filepath)
                return filepath
            return None

        # Generate files
        profile_avatar = generate_dummy_image('media/profile/avatar.png', 'Alexander Wright', '#6366f1')
        proj1_img = generate_dummy_image('media/projects/proj1.png', 'E-Commerce Platform', '#3b82f6')
        proj2_img = generate_dummy_image('media/projects/proj2.png', 'DevOps Automations', '#10b981')
        proj3_img = generate_dummy_image('media/projects/proj3.png', 'AI NLP Classifier', '#8b5cf6')
        blog1_img = generate_dummy_image('media/blog/blog1.png', 'Django 6 Features', '#f59e0b')
        blog2_img = generate_dummy_image('media/blog/blog2.png', 'Modern CSS Guide', '#ec4899')

        # 2. Create Profile
        Profile.objects.all().delete()
        profile = Profile.objects.create(
            name="Alexander Wright",
            title="Lead Software Engineer & Django Architect",
            bio="I am a software engineer specializing in building high-performance web backends, secure database architectures, and responsive interactive web frontends. Passionate about automated testing and system scalability.",
            email="alexander.wright@example.com",
            phone="+1 (555) 123-4567",
            location="San Francisco, CA",
            github="https://github.com",
            linkedin="https://linkedin.com",
            twitter="https://twitter.com",
            avatar='profile/avatar.png' if profile_avatar else None
        )
        self.stdout.write(self.style.SUCCESS('Profile created.'))

        # 3. Create Skills
        Skill.objects.all().delete()
        skills_data = [
            # Frontend
            ('Python & Django', 92, 'backend', 1),
            ('PostgreSQL & SQL', 85, 'backend', 2),
            ('Docker & DevOps', 78, 'devops', 3),
            ('AWS Cloud Solutions', 75, 'devops', 4),
            ('Vanilla JS (ES6+)', 88, 'frontend', 5),
            ('HTML5 & CSS3 Animations', 90, 'frontend', 6),
            ('Git & GitHub Action CI/CD', 85, 'tools', 7),
            ('Agile & Scrum Method', 80, 'tools', 8),
        ]
        for name, prof, cat, order in skills_data:
            Skill.objects.create(name=name, proficiency=prof, category=cat, order=order)
        self.stdout.write(self.style.SUCCESS('Skills created.'))

        # 4. Create Experiences
        Experience.objects.all().delete()
        Experience.objects.create(
            company="NexTech Solutions",
            role="Senior Backend Engineer",
            location="San Francisco, CA",
            start_date=timezone.datetime(2023, 6, 1).date(),
            is_current=True,
            description="Designed and scaled Django-based APIs supporting 50,000+ daily active users.\nMigrated database schemas to PostgreSQL and optimized query paths, decreasing page loading index by 35%.\nOrchestrated DevOps pipeline migrations from Travis CI to GitHub Actions, automating deployments on AWS ECS."
        )
        Experience.objects.create(
            company="WebLaunch Tech",
            role="Software Engineer",
            location="Austin, TX",
            start_date=timezone.datetime(2021, 3, 1).date(),
            end_date=timezone.datetime(2023, 5, 30).date(),
            is_current=False,
            description="Built custom web views, dashboards, and automated email reporting using Django and celery task queues.\nDeveloped responsive glassmorphic interfaces with custom interactive elements using vanilla JS and CSS.\nCollaborated directly with product teams to build modular REST APIs and integrate payment processors."
        )
        self.stdout.write(self.style.SUCCESS('Experiences created.'))

        # 5. Create Education
        Education.objects.all().delete()
        Education.objects.create(
            school="University of California, Berkeley",
            degree="M.S. in Computer Science",
            field_of_study="Distributed Systems & Software Engineering",
            location="Berkeley, CA",
            start_date=timezone.datetime(2019, 9, 1).date(),
            end_date=timezone.datetime(2021, 1, 15).date(),
            description="Specialized in cloud microservices and query optimizations. Graduate teaching assistant for Introduction to Database Systems."
        )
        Education.objects.create(
            school="University of Texas at Austin",
            degree="B.S. in Computer Science",
            field_of_study="Software Engineering",
            location="Austin, TX",
            start_date=timezone.datetime(2015, 9, 1).date(),
            end_date=timezone.datetime(2019, 5, 20).date(),
            description="Graduated Magna Cum Laude. Member of the Software Engineering Club and ACM Chapter."
        )
        self.stdout.write(self.style.SUCCESS('Education entries created.'))

        # 6. Create Projects
        Project.objects.all().delete()
        p1 = Project.objects.create(
            title="SaaS E-Commerce Core API",
            summary="A multitenant e-commerce API built with Django REST framework featuring Stripe subscriptions and catalog management.",
            description="This application provides a comprehensive backend solution for modern SaaS-styled digital commerce platforms. Key features include:\n- Secure Stripe subscription and payment gateway integrations.\n- Multi-tenant database schema layout utilizing PostgreSQL schemas.\n- Comprehensive API documentation generated with Swagger/OpenAPI.\n- Over 90% test coverage using Django unit tests and automated mock runs.",
            technologies="Django, REST API, Stripe, PostgreSQL, Docker",
            github_url="https://github.com",
            live_url="https://example.com",
            is_featured=True,
            order=1,
            featured_image='projects/proj1.png' if proj1_img else None
        )
        p2 = Project.objects.create(
            title="GitOps Kubernetes Cluster Orchestrator",
            summary="Automated Kubernetes deployments using ArgoCD, Terraform, and GitHub Actions.",
            description="An orchestration project to support zero-downtime microservice deployments under production environments. Key features include:\n- Infra-as-code deployment on AWS EKS cluster configurations using Terraform modules.\n- Deployment controls handled via GitOps using ArgoCD integrations.\n- Configured horizontal pod autoscalers based on Prometheus metrics.",
            technologies="Terraform, Kubernetes, ArgoCD, AWS, GitHub Actions",
            github_url="https://github.com",
            is_featured=True,
            order=2,
            featured_image='projects/proj2.png' if proj2_img else None
        )
        p3 = Project.objects.create(
            title="AI NLP Sentiment Classifier",
            summary="Machine learning text analysis model served via Django API and a responsive vanilla dashboard.",
            description="A text classification service processing millions of items. Features include:\n- Custom NLP models built with PyTorch and fine-tuned on customer reviews.\n- Django view routing providing endpoints with sub-100ms response times.\n- Front-end visuals leveraging animated glassmorphic cards and CSS timelines.",
            technologies="Python, PyTorch, Django, JavaScript, CSS3",
            github_url="https://github.com",
            live_url="https://example.com",
            is_featured=False,
            order=3,
            featured_image='projects/proj3.png' if proj3_img else None
        )
        self.stdout.write(self.style.SUCCESS('Projects created.'))

        # 7. Create Blog Categories and Posts
        Category.objects.all().delete()
        Post.objects.all().delete()

        cat_dev = Category.objects.create(name="Web Development")
        cat_ops = Category.objects.create(name="DevOps & Cloud")

        post1 = Post.objects.create(
            title="Top 5 Hidden Features in Django 6.0",
            summary="An in-depth look at performance upgrades, database connection pooling improvements, and template changes in the latest Django release.",
            body="Django 6.0 introduces outstanding features that streamline developer experience and optimize execution patterns.\n\n## 1. Database Connection Pooling\nWith built-in pooling, you no longer require PgBouncer for basic connection reuse. Simply modify your settings to hold active connections.\n\n## 2. Advanced Form Rendering\nDjango 6.0 offers highly customizable form rendering defaults out of the box, making HTML class bindings cleaner.\n\n## 3. Template Performance\nThe templates engine has been refactored to compile block layouts up to 15% faster.\n\nEnjoy writing clean Django applications!",
            author=admin_user,
            category=cat_dev,
            tags="Django, Python, Backend",
            status='published',
            published_date=timezone.now(),
            featured_image='blog/blog1.png' if blog1_img else None
        )

        post2 = Post.objects.create(
            title="The Guide to Custom CSS Glassmorphism",
            summary="Learn how to style premium, glassy layouts with backdrop filters, thin translucent borders, and subtle glowing dropshadows.",
            body="Glassmorphism has taken the design world by storm. It looks sleek, premium, and futuristic.\n\n## Core Principles of Glassmorphism:\n1. Translucent background (e.g. `rgba(255, 255, 255, 0.05)`)\n2. Back-drop blur (`backdrop-filter: blur(10px)`)\n3. A thin, light border to define edges\n4. Subtle shadow for depth.\n\nTry integrating this system in your modern portfolio websites!",
            author=admin_user,
            category=cat_dev,
            tags="CSS, Design, FrontEnd",
            status='published',
            published_date=timezone.now() - timezone.timedelta(days=2),
            featured_image='blog/blog2.png' if blog2_img else None
        )

        self.stdout.write(self.style.SUCCESS('Blog Categories and Posts created.'))

        # 8. Create Certificates
        Certificate.objects.all().delete()
        Certificate.objects.create(
            name="AWS Certified Solutions Architect – Associate",
            issuing_organization="Amazon Web Services (AWS)",
            issue_date=timezone.datetime(2025, 4, 15).date(),
            credential_id="AWS-ASA-998877",
            credential_url="https://aws.amazon.com/certification/",
            order=1
        )
        Certificate.objects.create(
            name="Professional Scrum Master I (PSM I)",
            issuing_organization="Scrum.org",
            issue_date=timezone.datetime(2024, 11, 20).date(),
            credential_id="SCRUM-PSM-112233",
            credential_url="https://www.scrum.org",
            order=2
        )
        self.stdout.write(self.style.SUCCESS('Certificates created.'))

        # 9. Create Testimonials
        Testimonial.objects.all().delete()
        Testimonial.objects.create(
            client_name="Sarah Jenkins",
            client_title="Director of Engineering at NexTech Solutions",
            quote="Alexander is an outstanding engineer who consistently delivers reliable and highly optimized software. His expertise in database architecture and Django helped us scale our SaaS product by 300%.",
            order=1
        )
        Testimonial.objects.create(
            client_name="David Chen",
            client_title="Product Manager at WebLaunch Tech",
            quote="Working with Alexander was a pleasure. He has a rare combination of strong system architectural thinking and an eye for premium UI/UX design. Highly recommended!",
            order=2
        )
        self.stdout.write(self.style.SUCCESS('Testimonials created.'))

        self.stdout.write(self.style.SUCCESS('Database pre-population completed successfully!'))
