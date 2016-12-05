from django.db import models
from django.contrib.auth.models import User


def getCourseData(courseID, type=None):
    if type is None:
        return 0
    elif type == 'average-grade':
        return 90

def getRisk(studentID):
    # do something-else

    return 0.5

def getAssessment(studentID):
    # get data from outside db
    return 90
