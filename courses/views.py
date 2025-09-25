# courses/views.py
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, Enrollment
from .forms import CourseForm
from accounts.models import StudentProfile


# ======================
#   Admin Course Management
# ======================

class ManageCoursesView(LoginRequiredMixin, View):
    """
    Admin-only view to list and manage all courses.
    """
    template_name = "courses/manage_courses.html"

    def get(self, request):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can manage courses.")
        courses = Course.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"courses": courses})


class AddCourseView(LoginRequiredMixin, View):
    """
    Admin-only view to add a new course.
    """
    template_name = "courses/add_course.html"

    def get(self, request):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can add courses.")
        form = CourseForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can add courses.")
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect("courses:manage_courses")
        return render(request, self.template_name, {"form": form})


class EditCourseView(LoginRequiredMixin, View):
    """
    Admin-only view to edit an existing course.
    """
    template_name = "courses/edit_course.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can edit courses.")
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=course)
        return render(request, self.template_name, {"form": form, "course": course})

    def post(self, request, pk):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can edit courses.")
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect("courses:manage_courses")
        return render(request, self.template_name, {"form": form, "course": course})


class DeleteCourseView(LoginRequiredMixin, View):
    """
    Show delete confirmation (GET) and perform deletion (POST).
    """
    template_name = "courses/delete_course.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can delete courses.")
        course = get_object_or_404(Course, pk=pk)
        return render(request, self.template_name, {"course": course})

    def post(self, request, pk):
        if not request.user.is_admin:
            return HttpResponseForbidden("Only admin can delete courses.")
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect("courses:manage_courses")


# ======================
#   Course Browsing
# ======================

class CourseListView(LoginRequiredMixin, View):
    """
    View for students/admins to list all available courses.
    Also includes favorites if the user is a student.
    """
    template_name = "courses/course_list.html"

    def get(self, request):
        qs = Course.objects.all().order_by("-created_at")
        favorite_ids = []
        if hasattr(request.user, "studentprofile"):
            profile = request.user.studentprofile
            favorite_ids = profile.favorite_courses.values_list("id", flat=True)
        return render(
            request,
            self.template_name,
            {"courses": qs, "favorite_ids": set(favorite_ids)},
        )


class CourseDetailView(LoginRequiredMixin, View):
    """
    View for displaying detailed information about a single course.
    """
    template_name = "courses/course_detail.html"

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        favorite_ids = set()
        if hasattr(request.user, "studentprofile"):
            favorite_ids = set(request.user.studentprofile.favorite_courses.values_list("id", flat=True))
        return render(request, self.template_name, {"course": course, "favorite_ids": favorite_ids})


# ======================
#   Favorites (supports GET + POST)
# ======================

class ToggleFavoriteView(LoginRequiredMixin, View):
    """
    Toggle favorite status of a course for students only.
    Supports both GET (link) and POST (form).
    """

    def post(self, request, pk):
        return self._toggle(request, pk)

    def get(self, request, pk):
        return self._toggle(request, pk)

    def _toggle(self, request, pk):
        if not request.user.is_student:
            return HttpResponseForbidden("Only students can favorite courses.")

        course = get_object_or_404(Course, pk=pk)
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        if profile.favorite_courses.filter(pk=course.pk).exists():
            profile.favorite_courses.remove(course)
            messages.info(request, f"Removed {course.title} from favorites.")
        else:
            profile.favorite_courses.add(course)
            messages.success(request, f"Added {course.title} to favorites.")

        # Redirect to the previous page if available
        return redirect(request.META.get("HTTP_REFERER", "courses:course_list"))


# ======================
#   Enrollments
# ======================

class EnrollmentListView(LoginRequiredMixin, ListView):
    """
    Admin view: list all student enrollments.
    """
    model = Enrollment
    template_name = "courses/enrollments_list.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        return Enrollment.objects.all().select_related("student", "course")


class StudentEnrollmentsView(LoginRequiredMixin, ListView):
    """
    Student view: list the logged-in student's enrollments.
    """
    model = Enrollment
    template_name = "courses/my_courses.html"
    context_object_name = "my_courses"

    def get_queryset(self):
        return (
            Enrollment.objects.filter(student=self.request.user)
            .select_related("course")
        )
