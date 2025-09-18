from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Favorite


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"You have enrolled in {course.title}.")
    return redirect("accounts:home")


@login_required
def add_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Favorite.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"{course.title} added to favorites ❤️")
    return redirect("accounts:home")


@login_required
def remove_enrollment(request, course_id):
    Enrollment.objects.filter(student=request.user, course_id=course_id).delete()
    messages.warning(request, "You have unenrolled from the course.")
    return redirect("accounts:home")


@login_required
def remove_favorite(request, course_id):
    Favorite.objects.filter(student=request.user, course_id=course_id).delete()
    messages.warning(request, "Removed from favorites.")
    return redirect("accounts:home")
