from django.contrib import admin
from .models import Instructor, Course, Student
# Register your models here.
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Student)
