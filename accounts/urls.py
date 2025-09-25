from django.urls import path
from .views import (
    LandingView, RegisterView, CustomLoginView, CustomLogoutView,
    ProfileView, ManageUsersView, EditUserView, DeleteUserView,
    PasswordResetRequestView, PasswordResetConfirmView, PasswordResetDoneView,
    DashboardView
)

app_name = "accounts"

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # admin user management
    path("manage_users/", ManageUsersView.as_view(), name="manage_users"),
    path("edit_user/<int:pk>/", EditUserView.as_view(), name="edit_user"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),

    # password reset (OTP)
    path("reset_password/", PasswordResetRequestView.as_view(), name="reset_password"),
    path("reset_password/done/", PasswordResetDoneView.as_view(), name="reset_password_done"),
    path("reset_password/confirm/", PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
]
