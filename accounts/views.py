from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import User
from .forms import UserRegisterForm, UserLoginForm


# ✅ Register new user
class RegisterView(SuccessMessageMixin, CreateView):
    """Handles user registration."""
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
    success_message = "Your account was created successfully. Please login."


# ✅ Custom login
class CustomLoginView(LoginView):
    """Custom login view with form validation."""
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def get_success_url(self):
        # After login → dashboard
        return reverse_lazy("accounts:dashboard")


# ✅ Custom logout
class CustomLogoutView(LogoutView):
    """Logs out user and redirects to login page."""
    next_page = reverse_lazy("accounts:login")


# ✅ Dashboard (role based)
class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view. Shows enrolled/favorite/available courses for students."""
    template_name = "accounts/dashboard.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_admin:
            # Enrolled + Favorite courses
            enrolled_courses = self.request.user.enrollments.select_related("course")
            favorite_courses = self.request.user.favorites.select_related("course")

            # IDs of enrolled courses
            enrolled_ids = enrolled_courses.values_list("course_id", flat=True)

            # Available courses = all courses not enrolled
            from courses.models import Course
            available_courses = Course.objects.exclude(id__in=enrolled_ids)

            context["enrolled_courses"] = enrolled_courses
            context["favorite_courses"] = favorite_courses
            context["available_courses"] = available_courses
        else:
            # For admins → keep empty (or later add stats)
            context["enrolled_courses"] = []
            context["favorite_courses"] = []
            context["available_courses"] = []

        return context


# ✅ Landing page → smart redirect
class LandingPageView(TemplateView):
    """
    Root page: decides where to send user.
    - Logged in → dashboard
    - Not logged in → login
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return redirect("accounts:login")
