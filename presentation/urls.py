from django.conf.urls import include, url
import presentation.views as views
from .models import Instructor, Student, Course
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def init():
    try:
        user = User.objects.create_user(username='test', password='1234qwer')
        user_1 =  User.objects.create_user(username='test_1', password='1234qwer')
        g = Group.objects.get(name='Instructors')
        g.user_set.add(user)
        g.user_set.add(user_1)
        instructor = Instructor.objects.create(user=user)
        instructor_1 = Instructor.objects.create(user=user_1)
        course = Course.objects.create(name='test', instructor=instructor,average=10)
        course_1 = Course.objects.create(name='test_1', instructor=instructor,average=15)
        course_2 = Course.objects.create(name='test_2', instructor=instructor,average=13)
        student = Student.objects.create(enrolledCourse=course, risk = 0.2, grades = [80,80,80])
        student_1 = Student.objects.create(enrolledCourse=course, risk = 1, grades = [30,40,50])
        student_2 = Student.objects.create(enrolledCourse=course, risk = 0.5, grades = [40,40,50])
    except:
        pass


init()

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'(?P<userID>[0-9]+)$', views.index, name='index'),
    # url(r'(?P<userID>[0-9]+)/$(?P<courseID>[0-9]+)', views.course_index, name='course_index')
    # url(r'(?P<studentID>[0-9]+)', views.student_index, name='student_index')
]
