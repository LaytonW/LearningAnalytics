""" presetting data base manager
read the data files for course scores and student test scores
when receive request from models objects for display.
"""

from django.db import models
from django.contrib.auth.models import User


""" getting courseData from database,
input: course name and type,
type now can be "course_average" only for demo.
output: 0 if no type, average score for the specific course if type is defined.
"""


def getCourseData(courseName, type=None):
    # prevent none type calling
    if type is None:
        return 0
    elif type == 'average-grade':
        # read failed return 0
        average = 0
        # read data from outside result database with predefined schema
        with open('presentation/data/course_average.csv', 'r') as read:
            line = read.readline()
            while line:
                lineinfo = line.split(',')
                # filter the data only for the specified course
                if lineinfo[0] == courseName:
                    average = float(lineinfo[1].replace('\n', ''))
                    break
                else:
                    pass
                line = read.readline()
        return average

""" get risk factor from database,
input: student name and course name,
output: student risk factor for the particular course.
Note that the risk factor caculation logic has not been
use by machine learning method with implementation constraints.
"""


def getRisk(studentName, courseName):
    # call getCourseData and getAssessment function to facilitate
    courseAverage = getCourseData(courseName, 'average-grade')
    scoreList = getAssessment(studentName, courseName)
    count = 0
    # implement risk calculation logic in a simple way rather than machine learning
    for i in scoreList:
        if float(i) < courseAverage:
            count += 1
    return 0 + count / 3

""" get student assessment score from database,
input: student name and course name,
output: student all assessment scores in list.
"""


def getAssessment(studentName, courseName):
    # get data from outside db
    test = []
    # read data from outside result database with predefined schema
    with open('presentation/data/student_score.csv', 'r') as read:
        line = read.readline()
        while line:
            lineinfo = line.split(',')
            # filter the data only for the specified course and student
            if lineinfo[0] == studentName and lineinfo[1] == courseName:
                for score in lineinfo[2:-1]:
                    test.append(float(score.replace('\n', '')))
            else:
                pass
            line = read.readline()
    if len(test) != 0:
        return test
    # this is only protection for non-data feedback
    return [90.0, 85.5, 91.2]
