from django.db import models
from django.contrib.auth.models import User


def getCourseData(courseName, type=None):
    if type is None:
        return 0
    elif type == 'average-grade':
        #read failed return 0
        average = 0
        with open('course.data','r') as read:
            line = read.readline()
            while line:
                lineinfo = line.split(',')
                if lineinfo[1] == courseName:
                    average = lineinfo[2]
                    break
                else:
                    pass
                line = read.readline()
        return average

def getRisk(studentName, courseName):
    # do something-else
    courseAverage = getCourseData(courseName)
    return 0 + (sum(getAssessment(studentName, courseName)<courseAverage))/3


def getAssessment(studentName, courseName):
    # get data from outside db
    test = []
    with open('student.data','r') as read:
        line = read.readline()
        while line:
            lineinfo = line.split(',')
            if lineinfo[0] == studentName and lineinfo[1] == courseName:
                test.append(lineinfo[2])
            else:
                pass
            line = read.readline()
    if len(test) != 0:
        return test
    return [90.0,85.5,91.2]
