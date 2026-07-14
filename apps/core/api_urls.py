from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('profile/', api_views.profile_api, name='profile'),
    path('skills/', api_views.skills_api, name='skills'),
    path('experience/', api_views.experience_api, name='experience'),
    path('education/', api_views.education_api, name='education'),
    path('projects/', api_views.projects_api, name='projects'),
    path('projects/<slug:slug>/', api_views.project_detail_api, name='project_detail'),
    path('blog/', api_views.blog_api, name='blog'),
    path('blog/<slug:slug>/', api_views.blog_detail_api, name='blog_detail'),
    path('certificates/', api_views.certificates_api, name='certificates'),
    path('testimonials/', api_views.testimonials_api, name='testimonials'),
    path('contact/', api_views.contact_submit_api, name='contact'),
]
