""" views,
core handers for various messages,
covers all message handing logic for demo
"""


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
    """ index url handler,
    receive get request from instructor
    authenticate the user and start valid session
    """
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
    """ logout message url handler,
    receive logout method and terminate current session.k
    """
    auth.logout(request)
    return redirect('login')


@login_required
def index(request, userID):
    """ Instructor index url handler,
    receive request from success authentication
    return Instructor index page with all course
    listing course average score.
    """
    if request.method == 'GET':
        instructor = Instructor.objects.get(user__pk=userID)
        courseList = instructor.getCourses()
        studentList = []
        for student in instructor.getStudents():
            studentList.append(
                (
                    student,
                    "{:10.3f}".format(student.getOverallRisk()),
                    "{:10.3f}".format(student.getAverageGrade())
                )
            )
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        # update data
        for course in courseList:
            course.getCourseAverage()
        return render(
            request,
            'presentation/index.html',
            {
                'userID': userID,
                'courseList': courseList,
                'studentList': studentList[:5]
            }
        )


@login_required
def courses(request, userID):
    """courses collection url handler,
    receive request when instructor logs in,
    return all data of the courses taught by the instructor
    """
    if request.method == 'GET':
        instructor = Instructor.objects.get(user__pk=userID)
        courseList = instructor.getCourses()
        for course in courseList:
            course.getCourseAverage()
        return render(
            request,
            'presentation/courses.html',
            {'userID': userID, 'courseList': courseList}
        )


@login_required
def students(request, userID):
    """ students collection url handler,
    return all students who takes the courses
    taught by the instructor.
    """
    if request.method == 'GET':
        instructor = Instructor.objects.get(user__pk=userID)
        studentList = []
        for student in instructor.getStudents():
            studentList.append(
                (
                    student,
                    "{:10.3f}".format(student.getOverallRisk()),
                    "{:10.3f}".format(student.getAverageGrade())
                )
            )
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        return render(
            request,
            'presentation/students.html',
            {'userID': userID, 'studentList': studentList}
        )


@login_required
def course(request, userID):
    """ single course index url handler,
    receive request after Instructor choose particular course to view,
    return course index page with all student listing by risk factor descently
    """
    if request.method == "GET":
        courseID = request.GET.get('courseID')
        course = Course.objects.get(id=courseID)
        course.getCourseAverage()
        studentList = []
        # update data
        for student in course.getStudents():
            studentList.append(
                (
                    student,
                    "{:10.3f}".format(student.getRiskFactor(course.name)),
                    map(
                        lambda x: "{:10.3f}".format(x),
                        student.getGrade(course.name)
                    )
                )
            )
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        imgURL = "/images/image_average_quiz_grade_course_"
        imgURL += course.name.replace(' ', '_') + ".png"
        return render(
            request,
            'presentation/course.html',
            {
                'userID': userID, 'course': course,
                'studentList': studentList, 'imgURL': imgURL
            }
        )


@login_required
def student(request, userID):
    """ single student index url handler,
    receive request when Instructor choose particular student to view,
    return student index page with all test scores and other course info
    """
    if request.method == "GET":
        studentID = request.GET.get('studentID')
        student = Student.objects.get(id=studentID)
        courseID = request.GET.get('courseID')
        if courseID is not None:
            course = Course.objects.get(id=courseID)
            risk = "{:10.3f}".format(student.getRiskFactor(course.name))
            grades = map(
                lambda x: "{:10.3f}".format(x),
                student.getGrade(course.name)
            )
            imgURL = "/images/image_quiz_student_"
            imgURL += course.name.replace(' ', '_') + "_"
            imgURL += student.name.replace(' ', '_') + ".png"
            courseList = None
            avgRisk = None
            avgGrade = None
        else:
            avgRisk = "{:10.3f}".format(student.getOverallRisk())
            avgGrade = "{:10.3f}".format(student.getAverageGrade())
            courseList = []
            for course in student.getCourses():
                cImgURL = "/images/image_quiz_student_"
                cImgURL += course.name.replace(' ', '_') + "_"
                cImgURL += student.name.replace(' ', '_') + ".png"
                courseList.append(
                    (
                        course,
                        "{:10.3f}".format(student.getRiskFactor(course.name)),
                        map(
                            lambda x: "{:10.3f}".format(x),
                            student.getGrade(course.name)
                        ),
                        cImgURL
                    )
                )
            courseList.sort(key=(lambda x: x[1]), reverse=True)
            course = None
            risk = None
            grades = None
            imgURL = None
        return render(
            request,
            'presentation/student.html',
            {
                'userID': userID, 'student': student, 'imgURL': imgURL,
                'course': course, 'courseList': courseList, 'avgRisk': avgRisk,
                'avgGrade': avgGrade, 'risk': risk, 'grades': grades
            }
        )
