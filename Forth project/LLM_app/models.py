from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator

User = get_user_model()


class Course(models.Model):
    title       = models.CharField(max_length=150)
    slug        = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField()
    created_by  = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses"
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE,
                                    related_name="modules")
    title       = models.CharField(max_length=120)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course}: {self.title}"


class Lesson(models.Model):
    module      = models.ForeignKey(Module, on_delete=models.CASCADE,
                                    related_name="lessons")
    title       = models.CharField(max_length=120)
    content     = models.TextField()
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student     = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="enrollments")
    course      = models.ForeignKey(Course, on_delete=models.CASCADE,
                                    related_name="enrollments")
    joined_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} → {self.course}"


class Assignment(models.Model):
    lesson          = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                        related_name="assignments")
    title           = models.CharField(max_length=120)
    description     = models.TextField()
    due_date        = models.DateField()
    max_score       = models.PositiveIntegerField(default=100,
                        validators=[MinValueValidator(1)])

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment  = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                    related_name="submissions")
    student     = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="submissions")
    text        = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    score       = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student} – {self.assignment}"
