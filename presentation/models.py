from django.db import models
from django.contrib.auth.models import User
from .dataAnalysis import DataAnalyzer

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE
    )  # many-to-one
    def getCourseAverage(self,courseID):
        return DataAnalyzer.getCourseData(self.pk, type='average-grade')
    def __str__(self):
        return self.name


class Student(models.Model):
    enrolledCourse = models.ForeignKey(
        Course, on_delete=models.CASCADE
    )
    def getRiskFactor(self):
        return DataAnalyzer.getRisk(self.pk)
    def getGrade(self):
        return DataAnalyzer.getAssessment(self.pk)
