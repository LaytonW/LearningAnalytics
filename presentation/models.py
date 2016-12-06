
""" fundamental models for http server,
some data may need another file to save
through the class called DataAnalyzer
"""

from django.db import models
from django.contrib.auth.models import User
from .dataAnalysis import DataAnalyzer
from django.contrib.postgres.fields import ArrayField


""" instructor model,
handle login and signup
associate with course he or she teaches
"""


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def getCourses(self):
        return self.course_set.all()

""" course model,
store the course average data,
and future data could be addin easily
"""


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
            self.name, type='average-grade'
        )
        self.save()

    def __str__(self):
        return self.name

""" student model,
associate with class that he or she takes,
store the average score for display in student index,
also store the demo risk factor for display
"""


class Student(models.Model):
    name = models.CharField(max_length=200, default='default')
    enrolledCourse = models.ManyToManyField(Course)
    risk = models.FloatField(null=True)
    grades = ArrayField(models.FloatField(), null=True)

    def getCourses(self):
        return self.enrolledCourse.all()

    def getRiskFactor(self, courseName):
        self.risk = DataAnalyzer.getRisk(self.name, courseName)
        self.save()
    # def getAverageGrade(self):
    #     self.getGrade()
    #     self.save()

    def getGrade(self, courseName):
        self.grade = DataAnalyzer.getAssessment(self.name, courseName)
        self.save()
