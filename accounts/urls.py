from django.urls import path, include, reverse_lazy
from .views import (
    RegisterView, CustomLoginView, CustomLogoutView, DashboardView, LandingPageView,
    ManageUsersView, EditUserView, DeleteUserView, profile_view
)
from django.contrib.auth import views as auth_views

app_name = "accounts"

# ----------------------------
# Password reset URL patterns
# ----------------------------
password_reset_patterns = [
    path(
        "",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/reset_password.html",
            email_template_name="accounts/reset_password_email.html",
            success_url=reverse_lazy("accounts:password_reset_done")
        ),
        name="reset_password"
    ),
    path(
        "sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset_password_done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/reset_password_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete")
        ),
        name="password_reset_confirm"
    ),
    path(
        "complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/reset_password_complete.html"
        ),
        name="password_reset_complete"
    ),
]

# ----------------------------
# Main URL patterns
# ----------------------------
urlpatterns = [
    # Landing, Auth, Dashboard
    path("", LandingPageView.as_view(), name="landing"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # Profile
    path("profile/", profile_view, name="profile"),

    # Admin user management
    path("manage_users/", ManageUsersView.as_view(), name="manage_users"),
    path("edit_user/<int:pk>/", EditUserView.as_view(), name="edit_user"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),

    # Password reset
    path("reset_password/", include(password_reset_patterns)),
]
