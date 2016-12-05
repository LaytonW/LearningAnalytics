from django.db import models
from django.contrib.auth.models import User


def getCourseData(courseID, type=None):
    if type is None:
        return 0
    elif type == 'average-grade':
        #read failed return 0
        average = 0
        with open('course.data','r') as read:
            line = read.readline()
            while line:
                lineinfo = line.split(',')
                if lineinfo[1] == courseID:
                    average = lineinfo[2]
                    break
                else:
                    pass
                line = read.readline()
        return average

def getRisk(studentID):
    # do something-else

    return int(studentID)/10

def getAssessment(studentID, courseID):
    # get data from outside db
    test = []
    with open('student.data','r') as read:
        line = read.readline()
        while line:
            lineinfo = line.split(',')
            if lineinfo[0] == studentID and lineinfo[1] == courseID:
                test.append(lineinfo[2])
            else:
                pass
            line = read.readline()
    if len(test) != 0:
        return test
    return [90.0,85.5,91.2]
