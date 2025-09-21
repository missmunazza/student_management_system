from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

User = get_user_model()

# ----------------------------
# Registration
# ----------------------------
class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")
    success_message = "Your account was created successfully. Please login."


# ----------------------------
# Custom login/logout
# ----------------------------
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:dashboard")


class CustomLogoutView(LogoutView):
    # Use POST logout; next_page is optional if using GET method
    next_page = reverse_lazy("accounts:login")


# ----------------------------
# Dashboard
# ----------------------------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
    login_url = "accounts:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_admin:
            enrolled_courses = self.request.user.enrollments.select_related("course")
            favorite_courses = self.request.user.favorites.select_related("course")
            enrolled_ids = enrolled_courses.values_list("course_id", flat=True)

            from courses.models import Course
            available_courses = Course.objects.exclude(id__in=enrolled_ids)

            context.update({
                "enrolled_courses": enrolled_courses,
                "favorite_courses": favorite_courses,
                "available_courses": available_courses
            })
        else:
            context.update({
                "enrolled_courses": [],
                "favorite_courses": [],
                "available_courses": []
            })

        return context


# ----------------------------
# Landing page redirect
# ----------------------------
class LandingPageView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        return redirect("accounts:login")


# ----------------------------
# Admin: Manage Users
# ----------------------------
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin


class ManageUsersView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/manage_users.html"
    context_object_name = "users"


class EditUserView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    fields = ["name", "email", "is_active", "is_admin", "is_student"]
    template_name = "accounts/edit_user.html"
    success_url = reverse_lazy("accounts:manage_users")


class DeleteUserView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/delete_user.html"
    success_url = reverse_lazy("accounts:manage_users")


# ----------------------------
# Profile update
# ----------------------------
@login_required
def profile_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if name and email:
            request.user.name = name
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "All fields are required.")

    return render(request, "accounts/profile.html")
