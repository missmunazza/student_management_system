from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "name", "is_student", "is_admin", "is_active")
    list_filter = ("is_admin", "is_student", "is_active")
    ordering = ("email",)
    search_fields = ("email", "name")
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_admin", "is_student", "is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("OTP", {"fields": ("otp",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_student", "is_admin", "is_active"),
        }),
    )

admin.site.register(User, UserAdmin)
