# LLM_app/admin.py
from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Assignment, Submission

admin.site.register((Course, Module, Lesson, Enrollment, Assignment, Submission))
