from django.conf.urls import include, url
import presentation.views as views
from .models import Instructor, Student, Course
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def init():
    try:
        user = User.objects.create_user(username='hcwang', password='1234qwer')
        user_1 = User.objects.create_user(
            username='zrji', password='1234qwer'
        )
        g = Group.objects.get(name='Instructors')
        g.user_set.add(user)
        g.user_set.add(user_1)
        instructor = Instructor.objects.create(user=user)
        instructor_1 = Instructor.objects.create(user=user_1)
        course = Course.objects.create(
            name='Introduction to Software Engineering',
            instructor=instructor, average=10
        )
        course_1 = Course.objects.create(
            name='System and Network Programming',
            instructor=instructor, average=15
        )
        course_2 = Course.objects.create(
            name='Introduction to Mirco-economics',
            instructor=instructor, average=13
        )
        student = Student.objects.create(
            name='Zixu WANG',
            risk=0.2, grades=[80, 80, 80]
        )
        student.enrolledCourse.add(course)
        student.enrolledCourse.add(course_1)
        student_1 = Student.objects.create(
            name='Zhihan CHEN',
            risk=1, grades=[30, 40, 50])
        student_1.enrolledCourse.add(course)
        student_1.enrolledCourse.add(course_1)
        student_2 = Student.objects.create(
            name='Chang GAO', 
            risk=0.8, grades=[40, 40, 50])
        student_2.enrolledCourse.add(course)
        student_2.enrolledCourse.add(course_1)
    except:
        pass


init()

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
