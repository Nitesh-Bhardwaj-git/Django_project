from django import forms
from .models import Course, Lesson, Module, Assignment, Submission

class CourseForm(forms.ModelForm):
    class Meta:
        model  = Course
        fields = ("title", "description")

class ModuleForm(forms.ModelForm):
    class Meta:
        model  = Module
        fields = ("title", "order")

class LessonForm(forms.ModelForm):
    class Meta:
        model  = Lesson
        fields = ("title", "content", "order")

class AssignmentForm(forms.ModelForm):
    class Meta:
        model  = Assignment
        fields = ("title", "description", "due_date", "max_score")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model  = Submission
        fields = ("text",)
