# accounts/views.py
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import (
    UserRegisterForm, UserLoginForm, ProfileForm, AvatarForm,
    PasswordResetRequestForm, PasswordResetConfirmForm
)
from .models import StudentProfile
from courses.models import Course

User = get_user_model()

# ---------- Landing ----------
class LandingView(View):
    template_name = "accounts/landing.html"

    def get(self, request):
        # featured: just titles + descriptions (no course images shown on landing)
        featured = Course.objects.all().order_by("-created_at")[:6]

        if request.user.is_authenticated:
            profile = getattr(request.user, "studentprofile", None)
            favorite_ids = set(
                profile.favorite_courses.values_list("id", flat=True)
            ) if profile else set()
        else:
            favorite_ids = set()

        return render(request, self.template_name, {
            "featured": featured,
            "favorite_ids": favorite_ids,
        })


# ---------- Registration ----------
class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        form = UserRegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("accounts:login")
        return render(request, self.template_name, {"form": form})


# ---------- Login / Logout ----------
class CustomLoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("accounts:dashboard")
        return render(request, self.template_name, {"form": form})


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "Logged out.")
        return redirect("accounts:landing")


# ---------- Admin check mixin ----------
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


# ---------- Profile ----------
class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        profile_form = ProfileForm(instance=request.user)
        avatar_form = AvatarForm(
            instance=request.user.studentprofile
            if hasattr(request.user, "studentprofile") else None
        )
        return render(request, self.template_name, {
            "profile_form": profile_form,
            "avatar_form": avatar_form
        })

    def post(self, request):
        profile_form = ProfileForm(request.POST, instance=request.user)
        avatar_form = AvatarForm(
            request.POST, request.FILES,
            instance=request.user.studentprofile
            if hasattr(request.user, "studentprofile") else None
        )
        if profile_form.is_valid() and avatar_form.is_valid():
            profile_form.save()
            avatar_form.save()
            messages.success(request, "Profile updated successfully.")
            # Redirect to dashboard so user sees a different page after POST (PRG pattern)
            return redirect("accounts:dashboard")
        messages.error(request, "Please fix the errors below.")
        return render(request, self.template_name, {
            "profile_form": profile_form,
            "avatar_form": avatar_form
        })


# ---------- Admin User Management ----------
class ManageUsersView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "accounts/manage_users.html"

    def get(self, request):
        users = User.objects.all().order_by("-date_joined")
        return render(request, self.template_name, {"users": users})


class EditUserView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "accounts/edit_user.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ProfileForm(instance=user)
        return render(request, self.template_name, {"form": form, "user_obj": user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated.")
            return redirect("accounts:manage_users")
        return render(request, self.template_name, {"form": form, "user_obj": user})


class DeleteUserView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, "User deleted.")
        return redirect("accounts:manage_users")


# ---------- OTP Password Reset ----------
class PasswordResetRequestView(View):
    template_name = "accounts/reset_password.html"

    def get(self, request):
        return render(request, self.template_name, {"form": PasswordResetRequestForm()})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                messages.success(request, "If this email exists, an OTP has been sent.")
                return redirect("accounts:reset_password_done")

            otp = f"{random.randint(0, 999999):06d}"
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_mail(
                "Password reset OTP",
                f"Your OTP for password reset is: {otp}\n"
                f"It expires in {settings.OTP_EXPIRY_SECONDS // 60} minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            messages.success(request, "OTP sent to your email (console in dev).")
            return redirect(f"{reverse_lazy('accounts:reset_password_confirm')}?user_id={user.id}")

        return render(request, self.template_name, {"form": form})


class PasswordResetDoneView(TemplateView):
    template_name = "accounts/reset_password_done.html"


class PasswordResetConfirmView(View):
    template_name = "accounts/reset_password_confirm.html"

    def get(self, request):
        user_id = request.GET.get("user_id")
        if not user_id:
            messages.error(request, "Invalid password reset link.")
            return redirect("accounts:reset_password")
        form = PasswordResetConfirmForm(initial={"user_id": user_id})
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data["user_id"]
            otp = form.cleaned_data["otp"]
            new_password = form.cleaned_data["new_password1"]

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                form.add_error(None, "Invalid user.")
                return render(request, self.template_name, {"form": form})

            if not user.otp or user.otp != otp:
                form.add_error("otp", "Invalid OTP")
                return render(request, self.template_name, {"form": form})

            if user.otp_created_at and (timezone.now() - user.otp_created_at).total_seconds() > settings.OTP_EXPIRY_SECONDS:
                form.add_error("otp", "OTP expired")
                return render(request, self.template_name, {"form": form})

            user.set_password(new_password)
            user.otp = None
            user.otp_created_at = None
            user.save()

            messages.success(request, "Password reset successful. Please log in.")
            return redirect("accounts:login")

        if "user_id" in request.POST:
            form.fields["user_id"].initial = request.POST.get("user_id")

        return render(request, self.template_name, {"form": form})


# ---------- Dashboard ----------
class DashboardView(LoginRequiredMixin, View):
    template_name = "accounts/dashboard.html"

    def get(self, request):
        stats = {}
        recent_courses = Course.objects.all().order_by("-created_at")[:6]

        if request.user.is_admin:
            stats["students_count"] = User.objects.filter(is_student=True).count()
            stats["courses_count"] = Course.objects.all().count()
            stats["favorites_count"] = sum(
                p.favorite_courses.count()
                for p in StudentProfile.objects.all()
            )
            favorite_ids = set()
        else:
            profile = getattr(request.user, "studentprofile", None)
            favorites = profile.favorite_courses.all() if profile else Course.objects.none()
            stats["my_favorites_count"] = favorites.count()
            stats["courses_count"] = Course.objects.all().count()
            favorite_ids = set(favorites.values_list("id", flat=True))

        return render(request, self.template_name, {
            "stats": stats,
            "recent_courses": recent_courses,
            "favorite_ids": favorite_ids,
        })
