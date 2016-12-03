from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many-to-one


class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE
    )  # many-to-one

    def __str__(self):
        return self.name

class Student(models.Model):
    enrolledCourse = models.ForeignKey(
        Course, on_delete=models.CASCADE
    )
