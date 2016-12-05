from django.db import models
from django.contrib.auth.models import User
from .dataAnalysis import DataAnalyzer
from django.contrib.postgres.fields import ArrayField


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def getCourses(self):
        return self.course_set.all()


class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE
    )  # many-to-one
    average = models.FloatField(null=True)

    def getStudents(self):
        return self.student_set.all()

    def getCourseAverage(self):
        self.average = DataAnalyzer.getCourseData(
            self.pk, type='average-grade'
        )
        self.save()

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200, default='default')
    enrolledCourse = models.ManyToManyField(Course)
    risk = models.FloatField(null=True)
    grades = ArrayField(models.FloatField(), null=True)

    def getCourses(self):
        return self.enrolledCourse.all()

    def getRiskFactor(self):
        self.risk = DataAnalyzer.getRisk(self.pk)
        self.save()
    # def getAverageGrade(self):
    #     self.getGrade()
    #     self.save()

    def getGrade(self, courseID):
        self.grade = DataAnalyzer.getAssessment(self.pk, courseID)
        self.save()
