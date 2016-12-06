from django.conf.urls import include, url
import presentation.views as views
from .models import Instructor, Student, Course
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


""" database setting for demo,
check the database if it has data,
otherwise run setting up predefined data for basic functionalities testing.
"""


def init():
    try:
        # construct instructor:
        g = Group.objects.get(name='Instructors')
        with open('presentation/data/instructor.csv') as reader:
            line = reader.readline()
            while line:
                username = line.split(',')[0].strip()
                password = line.split(',')[1].replace('\n', '').strip()
                user = User.objects.create_user(
                    username=username, password=password)
                g.user_set.add(user)
                Instructor.objects.create(user=user)
                line = reader.readline()

        # # construct course
        with open('presentation/data/course.csv') as reader:
            line = reader.readline()
            while line:
                courseName = line.split(',')[0]
                username = line.split(',')[1].replace('\n', '')
                instructor = Instructor.objects.get(user__username=username)
                Course.objects.create(
                    name=courseName,
                    instructor=instructor, average=0
                )
                line = reader.readline()

        # # construct students
        with open('presentation/data/student.csv') as reader:
            line = reader.readline()
            studentList = line.split(',')
            for i in studentList:
                i = i.replace('\n', '')
                Student.objects.create(name=str(i), risk=0)

        # construct enrollment
        with open('presentation/data/enrollment.csv') as reader:
            line = reader.readline()
            while line:
                studentName = line.split(',')[0]
                courseName = line.split(',')[1].replace('\n', '')
                student = Student.objects.get(name=str(studentName))
                course = Course.objects.get(name=str(courseName))
                student.enrolledCourse.add(course)
                line = reader.readline()

    except Exception as e:
        print(e)


init()

"""url mapping,
listening all predefined url pattern,
map different message to corresponding view function
where request can be processed properly.
"""
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'(?P<userID>[0-9]+)/$', views.index, name='index'),
    url(r'(?P<userID>[0-9]+)/courses/$', views.courses, name='courses'),
    url(r'(?P<userID>[0-9]+)/students/$', views.students, name='students'),
    url(
        r'(?P<userID>[0-9]+)/course/$', views.course, name='course'
    ),
    url(
        r'(?P<userID>[0-9]+)/student/$', views.student, name='student'
    ),
]
