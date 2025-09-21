from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("my/", views.my_courses, name="my_courses"),
    path("<int:course_id>/", views.course_detail, name="detail"),
    path("<int:course_id>/enroll/", views.enroll_course, name="enroll"),
    path("<int:course_id>/unenroll/", views.remove_enrollment, name="unenroll"),
    path("<int:course_id>/favorite/", views.add_favorite, name="favorite"),
    path("<int:course_id>/unfavorite/", views.remove_favorite, name="unfavorite"),

    # Admin
    path("manage/", views.ManageCoursesView.as_view(), name="manage_courses"),
    path("add/", views.AddCourseView.as_view(), name="add_course"),
    path("<int:pk>/edit/", views.EditCourseView.as_view(), name="edit_course"),
    path("<int:pk>/delete/", views.DeleteCourseView.as_view(), name="delete_course"),
]
