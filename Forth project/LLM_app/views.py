from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Enrollment
from .forms import CourseForm


class CourseList(ListView):
    model               = Course
    template_name       = "LLM_app/course_list.html"
    context_object_name = "courses"


class CourseDetail(DetailView):
    model         = Course
    template_name = "LLM_app/course_detail.html"


class InstructorRequired(UserPassesTestMixin):
    """Only allow the course creator to edit/delete."""
    def test_func(self):
        course = self.get_object()
        return self.request.user == course.created_by


class CourseCreate(CreateView):
    model         = Course
    form_class    = CourseForm
    template_name = "LLM_app/course_form.html"
    success_url   = reverse_lazy("course-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CourseUpdate(UpdateView):
    model         = Course
    form_class    = CourseForm
    template_name = "LLM_app/course_form.html"
    success_url   = reverse_lazy("course-list")


class CourseDelete(DeleteView):
    model         = Course
    template_name = "LLM_app/course_delete.html"
    success_url   = reverse_lazy("course-list")


class EnrollView(RedirectView):
    """Student clicks 'Enroll'; record is created then redirect back."""
    def get_redirect_url(self, *args, **kwargs):
        course = Course.objects.get(pk=kwargs["pk"])
        Enrollment.objects.get_or_create(student=self.request.user, course=course)
        return reverse("course-detail", kwargs={"pk": course.pk})
