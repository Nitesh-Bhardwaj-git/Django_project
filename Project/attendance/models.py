from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time_marked = models.TimeField()
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"