from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    # Course list & detail
    path("", views.course_list, name="list"),  # all courses
    path("<int:course_id>/", views.course_detail, name="detail"),  # single course (optional)

    # Enrollment actions
    path("<int:course_id>/enroll/", views.enroll_course, name="enroll"),
    path("<int:course_id>/unenroll/", views.remove_enrollment, name="unenroll"),

    # Favorite actions
    path("<int:course_id>/favorite/", views.add_favorite, name="favorite"),
    path("<int:course_id>/unfavorite/", views.remove_favorite, name="unfavorite"),

    # ✅ New route
    path("my/", views.my_courses, name="my_courses"),
]
