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
        studentList.sort(key=(lambda x: x.risk), reverse=True)
        # update data
        for course in courseList:
            pass
            # course.getCourseAverage()
        return render(
            request,
            'presentation/index.html',
            {'courseList': courseList, 'studentList': studentList}
        )

#
# @login_required
# def course_index(request, courseID):
#     if request.method == "GET":
#         studentList = Student.objects.filter(enrolledCourse__pk=courseID)
#         #update data
#         for student in studentList:
#             student.getRiskFactor()
#             student.getGrade(courseID)
#         return render(
#           request, 'presentation/course.html', {'studentList': studentList}
#         )
#
#
# @login_required
# def studentIndex(request, studentID, courseID):
#     if request.method == "GET":
#         student = Student.objects.get(pk=studentID)
#         student.getGrade(courseID)
#         return render(
#           request, 'presentation/student.html', {'student': student}
#         )
