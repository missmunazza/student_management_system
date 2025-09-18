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
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
    success_message = "Your account was created successfully. Please login."


# ✅ Custom login
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse_lazy("accounts:home")  # after login → dashboard


# ✅ Custom logout
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


# ✅ Dashboard (role based)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If it's a student, attach extra info
        if not self.request.user.is_admin:
            context["enrolled_courses"] = self.request.user.enrollments.all()
            context["favorite_courses"] = self.request.user.favorites.all()
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
            return redirect("accounts:home")
        return redirect("accounts:login")
