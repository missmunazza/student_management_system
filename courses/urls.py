from django.urls import path
from .views import (
    ManageCoursesView, AddCourseView, EditCourseView, DeleteCourseView,
    CourseListView, CourseDetailView, ToggleFavoriteView, EnrollmentListView,
    StudentEnrollmentsView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("manage/", ManageCoursesView.as_view(), name="manage_courses"),
    path("add/", AddCourseView.as_view(), name="add_course"),
    path("edit/<int:pk>/", EditCourseView.as_view(), name="edit_course"),
    path("delete/<int:pk>/", DeleteCourseView.as_view(), name="delete_course"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("<int:pk>/toggle_favorite/", ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("enrollments/", EnrollmentListView.as_view(), name="enrollments_list"),
    path("my-courses/", StudentEnrollmentsView.as_view(), name="my_courses"),
]
