"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import sitemap_xml, robots_txt, service_worker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sw.js', service_worker, name='service_worker'),
    path('', include('apps.core.urls')),
    path('projects/', include('apps.projects.urls')),
    path('contact/', include('apps.contact.urls')),
    path('blog/', include('apps.blog.urls')),
]

# Custom Error Handlers
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
