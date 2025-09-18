from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("<int:course_id>/enroll/", views.enroll_course, name="enroll"),
    path("<int:course_id>/favorite/", views.add_favorite, name="favorite"),
    path("<int:course_id>/unenroll/", views.remove_enrollment, name="unenroll"),
    path("<int:course_id>/unfavorite/", views.remove_favorite, name="unfavorite"),
]
