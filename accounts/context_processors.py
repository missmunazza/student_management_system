# accounts/context_processors.py
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def current_profile(request):
    """
    Add current_profile and safe display fields to every template's context.
    Avoids repeated lookups and prevents template VariableDoesNotExist issues.
    """
    user = getattr(request, "user", None)
    profile = None
    display_name = None
    avatar_url = None
    email = None

    if user and user.is_authenticated:
        # Try to get StudentProfile if available
        try:
            profile = getattr(user, "studentprofile", None)
        except Exception:
            profile = None

        # Preferred display name order: user.name, get_full_name(), email, str(user)
        display_name = getattr(user, "name", None) or getattr(user, "get_full_name", lambda: None)()
        if not display_name:
            display_name = getattr(user, "email", None) or str(user)

        email = getattr(user, "email", None)

        if profile and getattr(profile, "avatar", None):
            try:
                avatar_url = profile.avatar.url
            except Exception:
                avatar_url = None

    return {
        "current_profile": profile,
        "current_user_display_name": display_name,
        "current_user_email": email,
        "current_user_avatar_url": avatar_url,
    }
