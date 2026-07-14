import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import F

from apps.portfolio.models import Profile, Skill, Experience, Education, Certificate, Testimonial
from apps.projects.models import Project
from apps.blog.models import Post
from apps.contact.forms import ContactForm

def get_absolute_media_url(request, file_field):
    if not file_field:
        return None
    return request.build_absolute_uri(file_field.url)

@require_GET
def profile_api(request):
    profile = Profile.objects.first()
    if not profile:
        return JsonResponse({'message': 'Profile not found'}, status=404)
        
    data = {
        'name': profile.name,
        'title': profile.title,
        'bio': profile.bio,
        'avatar': get_absolute_media_url(request, profile.avatar),
        'resume': get_absolute_media_url(request, profile.resume),
        'email': profile.email,
        'phone': profile.phone,
        'location': profile.location,
        'socials': {
            'github': profile.github,
            'linkedin': profile.linkedin,
            'twitter': profile.twitter
        }
    }
    return JsonResponse(data)

@require_GET
def skills_api(request):
    skills = Skill.objects.all()
    skills_list = []
    for skill in skills:
        skills_list.append({
            'name': skill.name,
            'proficiency': skill.proficiency,
            'category': skill.category,
            'category_display': skill.get_category_display(),
            'order': skill.order
        })
    return JsonResponse({'skills': skills_list})

@require_GET
def experience_api(request):
    experiences = Experience.objects.all()
    exp_list = []
    for exp in experiences:
        exp_list.append({
            'company': exp.company,
            'role': exp.role,
            'location': exp.location,
            'start_date': exp.start_date.isoformat(),
            'end_date': exp.end_date.isoformat() if exp.end_date else None,
            'is_current': exp.is_current,
            'description': exp.description,
            'description_points': exp.get_description_points()
        })
    return JsonResponse({'experiences': exp_list})

@require_GET
def education_api(request):
    education = Education.objects.all()
    edu_list = []
    for edu in education:
        edu_list.append({
            'school': edu.school,
            'degree': edu.degree,
            'field_of_study': edu.field_of_study,
            'location': edu.location,
            'start_date': edu.start_date.isoformat(),
            'end_date': edu.end_date.isoformat() if edu.end_date else None,
            'is_current': edu.is_current,
            'description': edu.description
        })
    return JsonResponse({'education': edu_list})

@require_GET
def projects_api(request):
    projects = Project.objects.all()
    proj_list = []
    for project in projects:
        proj_list.append({
            'title': project.title,
            'slug': project.slug,
            'summary': project.summary,
            'featured_image': get_absolute_media_url(request, project.featured_image),
            'technologies': project.get_tech_list(),
            'live_url': project.live_url,
            'github_url': project.github_url,
            'is_featured': project.is_featured,
            'order': project.order,
            'detail_url': request.build_absolute_uri(project.get_absolute_url())
        })
    return JsonResponse({'projects': proj_list})

@require_GET
def project_detail_api(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    gallery = []
    for img in project.images.all():
        gallery.append({
            'image': get_absolute_media_url(request, img.image),
            'caption': img.caption
        })

    data = {
        'title': project.title,
        'slug': project.slug,
        'summary': project.summary,
        'description': project.description,
        'featured_image': get_absolute_media_url(request, project.featured_image),
        'technologies': project.get_tech_list(),
        'live_url': project.live_url,
        'github_url': project.github_url,
        'is_featured': project.is_featured,
        'created_at': project.created_at.isoformat(),
        'gallery': gallery
    }
    return JsonResponse(data)

@require_GET
def blog_api(request):
    posts = Post.objects.filter(status='published')
    
    # Filter by category if query param is set
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Filter by tag if query param is set
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__icontains=tag)

    posts_list = []
    for post in posts:
        posts_list.append({
            'title': post.title,
            'slug': post.slug,
            'summary': post.summary,
            'featured_image': get_absolute_media_url(request, post.featured_image),
            'category': post.category.name if post.category else None,
            'tags': post.get_tag_list(),
            'views': post.views,
            'published_date': post.published_date.isoformat() if post.published_date else None,
            'reading_time': post.reading_time,
            'detail_url': request.build_absolute_uri(post.get_absolute_url())
        })
    return JsonResponse({'posts': posts_list})

@require_GET
def blog_detail_api(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Safe views increment
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()

    data = {
        'title': post.title,
        'slug': post.slug,
        'summary': post.summary,
        'body': post.body,
        'featured_image': get_absolute_media_url(request, post.featured_image),
        'category': post.category.name if post.category else None,
        'tags': post.get_tag_list(),
        'views': post.views,
        'published_date': post.published_date.isoformat() if post.published_date else None,
        'reading_time': post.reading_time,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat()
    }
    return JsonResponse(data)

@require_GET
def certificates_api(request):
    certs = Certificate.objects.all()
    certs_list = []
    for cert in certs:
        certs_list.append({
            'name': cert.name,
            'issuing_organization': cert.issuing_organization,
            'issue_date': cert.issue_date.isoformat(),
            'expiration_date': cert.expiration_date.isoformat() if cert.expiration_date else None,
            'credential_id': cert.credential_id,
            'credential_url': cert.credential_url,
            'logo': get_absolute_media_url(request, cert.logo)
        })
    return JsonResponse({'certificates': certs_list})

@require_GET
def testimonials_api(request):
    testimonials = Testimonial.objects.all()
    test_list = []
    for test in testimonials:
        test_list.append({
            'client_name': test.client_name,
            'client_title': test.client_title,
            'quote': test.quote,
            'client_avatar': get_absolute_media_url(request, test.client_avatar)
        })
    return JsonResponse({'testimonials': test_list})

@csrf_exempt
@require_http_methods(["POST"])
def contact_submit_api(request):
    # Parse payload
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        data = request.POST

    form = ContactForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your message has been sent successfully.'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)
