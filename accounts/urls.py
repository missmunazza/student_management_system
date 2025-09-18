from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    LandingPageView,
)

app_name = "accounts"

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),       # root smart redirect
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="home"),  # main dashboard
]
