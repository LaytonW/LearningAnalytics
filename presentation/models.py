
""" fundamental models for http server,
some data may need another file to save
through the class called DataAnalyzer
"""

from django.db import models
from django.contrib.auth.models import User
from .dataAnalysis import DataAnalyzer
from django.contrib.postgres.fields import ArrayField
from functools import reduce


class Instructor(models.Model):
    """ instructor model,
    handle login and signup
    associate with course he or she teaches
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def getCourses(self):
        return list(self.course_set.all())

    def getStudents(self):
        return reduce(
            lambda x, y: list(set(x + y)),
            map(lambda x: x.getStudents(), self.getCourses())
        )


class Course(models.Model):
    """ course model,
    store the course average data,
    and future data could be addin easily
    """
    name = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE
    )  # many-to-one
    average = models.FloatField(null=True)

    def getStudents(self):
        return list(self.student_set.all())

    def getCourseAverage(self):
        self.average = DataAnalyzer.getCourseData(
            self.name, type='average-grade'
        )
        self.save()

    def __str__(self):
        return self.name


class Student(models.Model):
    """ student model,
    associate with class that he or she takes,
    store the average score for display in student index,
    also store the demo risk factor for display
    """
    name = models.CharField(max_length=200, default='default')
    enrolledCourse = models.ManyToManyField(Course)

    def getCourses(self):
        return list(self.enrolledCourse.all())

    def getRiskFactor(self, courseName):
        return DataAnalyzer.getRisk(self.name, courseName)

    def getOverallRisk(self):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: self.getRiskFactor(x.name), self.getCourses())
        ) / float(len(self.getCourses()))

    def getGrade(self, courseName):
        return DataAnalyzer.getAssessment(self.name, courseName)

    def getAverageGrade(self):
        return reduce(
            lambda x, y: x + y,
            map(
                lambda z:
                    reduce(
                        lambda a, b: a + b,
                        self.getGrade(z.name)
                    ) / float(len(self.getGrade(z.name))),
                self.getCourses()
            )
        ) / float(len(self.getCourses()))
