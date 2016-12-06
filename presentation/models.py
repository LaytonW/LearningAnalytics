
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

    # get all courses the instructor teaches
    def getCourses(self):
        return list(self.course_set.all())

    # get all students who take the course taught by the instructor
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

    # get all student within the course
    def getStudents(self):
        return list(self.student_set.all())

    # get course average grade using DataAnalyzer
    def getCourseAverage(self):
        self.average = DataAnalyzer.getCourseData(
            self.name, type='average-grade'
        )
        self.save()

    # simple built in function to show name of course
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

    # get all course that the student has been enrolled
    def getCourses(self):
        return list(self.enrolledCourse.all())

    # get the risk factor for the student in particular course
    def getRiskFactor(self, courseName):
        return DataAnalyzer.getRisk(self.name, courseName)

    # get overall risk generated from all risk in the courses
    # that the student are taking
    def getOverallRisk(self):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: self.getRiskFactor(x.name), self.getCourses())
        ) / float(len(self.getCourses()))

    # get all quiz score in a list for student in a particular course
    def getGrade(self, courseName):
        return DataAnalyzer.getAssessment(self.name, courseName)

    # get average grade in all courses taken by the student
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
