from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, Favorite

# ----------------------------
# Course List & Detail
# ----------------------------
@login_required
def course_list(request):
    courses = Course.objects.all()
    enrolled_ids = request.user.enrollments.values_list("course_id", flat=True)
    favorite_ids = request.user.favorites.values_list("course_id", flat=True)
    return render(request, "courses/course_list.html", {
        "courses": courses,
        "enrolled_ids": enrolled_ids,
        "favorite_ids": favorite_ids,
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user.enrollments.filter(course=course).exists()
    is_favorite = request.user.favorites.filter(course=course).exists()
    return render(request, "courses/course_detail.html", {
        "course": course,
        "is_enrolled": is_enrolled,
        "is_favorite": is_favorite,
    })

@login_required
def my_courses(request):
    enrollments = request.user.enrollments.select_related("course")
    return render(request, "courses/my_courses.html", {"enrollments": enrollments})

# ----------------------------
# Enrollment
# ----------------------------
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f"You have successfully enrolled in {course.title}")
    else:
        messages.info(request, f"You are already enrolled in {course.title}")
    return redirect("accounts:dashboard")

@login_required
def remove_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    deleted, _ = Enrollment.objects.filter(student=request.user, course=course).delete()
    if deleted:
        messages.warning(request, f"You have unenrolled from {course.title}")
    else:
        messages.info(request, f"You were not enrolled in {course.title}")
    return redirect("accounts:dashboard")

# ----------------------------
# Favorites
# ----------------------------
@login_required
def add_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    favorite, created = Favorite.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f"{course.title} added to favorites")
    else:
        messages.info(request, f"{course.title} is already in your favorites")
    return redirect("accounts:dashboard")

@login_required
def remove_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    deleted, _ = Favorite.objects.filter(student=request.user, course=course).delete()
    if deleted:
        messages.warning(request, f"{course.title} removed from favorites")
    else:
        messages.info(request, f"{course.title} was not in your favorites")
    return redirect("accounts:dashboard")

# ----------------------------
# Admin: Manage Courses
# ----------------------------
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin

class ManageCoursesView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    template_name = "courses/manage_courses.html"
    context_object_name = "courses"

class AddCourseView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Course
    fields = ["title", "description"]
    template_name = "courses/add_course.html"
    success_url = reverse_lazy("courses:manage_courses")

class EditCourseView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Course
    fields = ["title", "description"]
    template_name = "courses/edit_course.html"
    success_url = reverse_lazy("courses:manage_courses")

class DeleteCourseView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/delete_course.html"
    success_url = reverse_lazy("courses:manage_courses")
