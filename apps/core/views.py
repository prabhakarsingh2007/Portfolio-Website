from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from apps.portfolio.models import Profile, Skill, Experience, Education, Certificate, Testimonial
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
    try:
        latest_posts = Post.objects.filter(status='published').order_by('-published_date')[:3]
    except Exception:
        latest_posts = Post.objects.all()[:3]
        
    # Top skills for the home page (e.g. top 6)
    skills = Skill.objects.all()[:6]
    
    # Testimonials
    testimonials = Testimonial.objects.all()
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'latest_posts': latest_posts,
        'skills': skills,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all().order_by('-start_date')
    education = Education.objects.all().order_by('-start_date')
    certificates = Certificate.objects.all()
    
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
        'certificates': certificates,
    }
    return render(request, 'about.html', context)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request, exception=None):
    return render(request, '500.html', status=500)

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

@require_GET
def sitemap_xml(request):
    urls = [
        {'loc': request.build_absolute_uri('/'), 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': request.build_absolute_uri('/about/'), 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': request.build_absolute_uri('/projects/'), 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': request.build_absolute_uri('/blog/'), 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': request.build_absolute_uri('/contact/'), 'changefreq': 'monthly', 'priority': '0.7'},
    ]
    for project in Project.objects.all():
        urls.append({
            'loc': request.build_absolute_uri(project.get_absolute_url()),
            'changefreq': 'monthly',
            'priority': '0.7'
        })
    for post in Post.objects.filter(status='published'):
        urls.append({
            'loc': request.build_absolute_uri(post.get_absolute_url()),
            'changefreq': 'weekly',
            'priority': '0.8'
        })

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{url["loc"]}</loc>')
        xml_parts.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{url["priority"]}</priority>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')

    return HttpResponse("\n".join(xml_parts), content_type="application/xml")

@require_GET
def service_worker(request):
    sw_js = """const CACHE_NAME = 'antigravity-portfolio-v1';
const ASSETS = [
    '/',
    '/about/',
    '/projects/',
    '/blog/',
    '/contact/',
    '/static/css/style.css',
    '/static/css/responsive.css',
    '/static/css/animation.css',
    '/static/js/main.js',
    '/static/js/theme.js',
    '/static/js/animation.js',
    '/static/manifest.json'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});"""
    return HttpResponse(sw_js, content_type="application/javascript")
