from django.shortcuts import render
from apps.portfolio.models import Profile, Skill, Experience, Education
from apps.projects.models import Project
from apps.blog.models import Post

def home(request):
    profile = Profile.objects.first()
    # Get top 3 featured projects
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    if not featured_projects.exists():
        # Fallback if no projects are marked as featured
        featured_projects = Project.objects.all()[:3]
        
    # Get top 3 latest published blog posts
    latest_posts = Post.objects.filter(status='published').order_index() if hasattr(Post.objects, 'order_index') else Post.objects.filter(status='published').order_by('-created_at')[:3]
    # Check if Post has status and created_at field
    try:
        latest_posts = Post.objects.filter(status='published').order_by('-published_date')[:3]
    except Exception:
        latest_posts = Post.objects.all()[:3]
        
    # Top skills for the home page (e.g. top 6)
    skills = Skill.objects.all()[:6]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'latest_posts': latest_posts,
        'skills': skills,
    }
    return render(request, 'home.html', context)

def about(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all().order_by('-start_date')
    education = Education.objects.all().order_by('-start_date')
    
    # Categorize skills
    skills_by_category = {}
    for skill in skills:
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
        
    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
        'education': education,
    }
    return render(request, 'about.html', context)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request, exception=None):
    return render(request, '500.html', status=500)
