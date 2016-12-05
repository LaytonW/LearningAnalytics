from django.shortcuts import render_to_response, render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Course, Instructor, Student
from django.contrib.auth.models import User, Group


def login(request):
    if request.method == 'GET':
        return render(request, 'presentation/login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.POST.get('action') == 'LOGIN':
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.groups.filter(name='Instructors').exists():
                return JsonResponse({
                    "result": True,
                    "url": str(user.id)
                })
        return JsonResponse({"result": False})
    elif request.POST.get('action') == 'REGISTER':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"result": False, "errno": -1})
        else:
            newUser = User.objects.create_user(
                username=username, password=password,
                first_name=firstName, last_name=lastName
            )
            newUser.save()
            instructorGroup = Group.objects.get(name='Instructors')
            instructorGroup.user_set.add(newUser)
            instructorGroup.save()
            auth.login(request, newUser)
            return JsonResponse({
                "result": True,
                "url": str(newUser.id)
            })


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def index(request, userID):
    if request.method == 'GET':
        courseList = list(Instructor.objects.get(user__pk=userID).getCourses())
        studentList = []
        for course in courseList:
            studentList.extend(list(course.getStudents()))
        for student in studentList:
            pass
            # student.getRiskFactor()
            # student.getGrade()
        studentList = list(set(studentList))
        studentList.sort(key=(lambda x: x.risk), reverse=True)
        # update data
        for course in courseList:
            pass
            # course.getCourseAverage()
        return render(
            request,
            'presentation/index.html',
            {
                'userID': userID,
                'courseList': courseList,
                'studentList': studentList
            }
        )


@login_required
def courses(request, userID):
    if request.method == 'GET':
        courseList = list(Instructor.objects.get(user__pk=userID).getCourses())
        for course in courseList:
            pass
            # course.getCourseAverage()
        return render(
            request,
            'presentation/courses.html',
            {'userID': userID, 'courseList': courseList}
        )


@login_required
def students(request, userID):
    if request.method == 'GET':
        courseList = list(Instructor.objects.get(user__pk=userID).getCourses())
        studentDict = {}
        for course in courseList:
            studentDict[course.name] = list(course.getStudents())
        for courseName, studentList in studentDict.items():
            # student.getRiskFactor()
            # student.getGrade()
            studentList.sort(key=(lambda x: x.risk), reverse=True)
        return render(
            request,
            'presentation/students.html',
            {'userID': userID, 'studentDict': studentDict}
        )


@login_required
def course(request, userID):
    if request.method == "GET":
        courseID = request.GET.get('courseID')
        course = Course.objects.get(id=courseID)
        studentList = list(course.getStudents())
        # update data
        for student in studentList:
            pass
            # student.getRiskFactor()
            # student.getGrade(courseID)
        studentList.sort(key=(lambda x: x.risk), reverse=True)
        return render(
          request,
          'presentation/course.html',
          {'userID': userID, 'course': course, 'studentList': studentList}
        )


@login_required
def student(request, userID):
    if request.method == "GET":
        studentID = request.GET.get('studentID')
        student = Student.objects.get(id=studentID)
        courseList = list(student.getCourses())
        # student.getRiskFactor()
        # student.getGrade(courseID)
        return render(
          request,
          'presentation/student.html',
          {'userID': userID, 'student': student, 'courseList': courseList}
        )
