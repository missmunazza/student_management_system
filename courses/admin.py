from django.contrib import admin
from .models import Course, Favorite, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "created_at")
    list_filter = ("created_at",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_on", "grade")
    list_filter = ("enrolled_on", "grade")
    search_fields = ("student__username", "course__title")
