from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="e.g. Full Stack Developer & UI/UX Designer")
    bio = models.TextField()
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='profile/', blank=True, null=True, help_text="Upload PDF resume")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend Development'),
        ('backend', 'Backend Development'),
        ('devops', 'DevOps & Cloud'),
        ('tools', 'Tools & Methodologies'),
    ]
    name = models.CharField(max_length=50)
    proficiency = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Enter proficiency as a percentage (1-100)"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='frontend')
    order = models.PositiveIntegerField(default=0, help_text="Sort order")

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"

class Experience(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Detailed description of responsibilities/projects. Separate points by newline.")

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_description_points(self):
        """Splits description by newlines for clean bulleted rendering in templates."""
        if not self.description:
            return []
        return [point.strip() for point in self.description.split('\n') if point.strip()]

class Education(models.Model):
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, help_text="Relevant coursework, activities, honors.")

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} from {self.school}"

class Certificate(models.Model):
    name = models.CharField(max_length=150)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='certificates/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Sort order")

    class Meta:
        ordering = ['order', '-issue_date']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, help_text="e.g. CEO at Acme Corp")
    quote = models.TextField()
    client_avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Sort order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Testimonial from {self.client_name}"
