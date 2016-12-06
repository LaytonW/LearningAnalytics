"""Registration of models for learning analytics demo"""

from django.contrib import admin
from .models import Instructor, Course, Student

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Student)
