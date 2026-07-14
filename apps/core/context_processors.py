from django.utils import timezone
from apps.portfolio.models import Profile

def global_context(request):
    # Try to get profile if it exists, otherwise default values
    try:
        profile = Profile.objects.first()
    except Exception:
        profile = None

    context = {
        'current_year': timezone.now().year,
        'site_title': 'Antigravity Portfolio',
        'social_github': profile.github if profile and profile.github else 'https://github.com',
        'social_linkedin': profile.linkedin if profile and profile.linkedin else 'https://linkedin.com',
        'social_twitter': profile.twitter if profile and profile.twitter else 'https://twitter.com',
        'social_instagram': 'https://instagram.com',
        'contact_email': profile.email if profile and profile.email else 'contact@example.com',
        'profile': profile,
    }
    return context
