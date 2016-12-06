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
        # Respond to GET login page.
        return render(request, 'presentation/login.html')
    # Get username and password via HTTP POST.
    username = request.POST.get('username')
    password = request.POST.get('password')
    # If login is requested.
    if request.POST.get('action') == 'LOGIN':
        # Try to authenticate user.
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # User authenticated.
            auth.login(request, user)
            # If user is a ninstructor.
            if user.groups.filter(name='Instructors').exists():
                # User authenticated as an instructor,
                # return JSON response to confirm.
                return JsonResponse({
                    "result": True,
                    "url": str(user.id)
                })
        # Authentication failed, return failure.
        return JsonResponse({"result": False})
    # If register is requested.
    elif request.POST.get('action') == 'REGISTER':
        # Get registration data.
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        # If user already exists, return error.
        if User.objects.filter(username=username).exists():
            return JsonResponse({"result": False, "errno": -1})
        else:
            # Create new user and add to instructor group.
            newUser = User.objects.create_user(
                username=username, password=password,
                first_name=firstName, last_name=lastName
            )
            newUser.save()
            instructorGroup = Group.objects.get(name='Instructors')
            instructorGroup.user_set.add(newUser)
            instructorGroup.save()
            # Login the newly registered user.
            auth.login(request, newUser)
            # Registration success, return JSON response.
            return JsonResponse({
                "result": True,
                "url": str(newUser.id)
            })


def logout(request):
    """ logout message url handler,
    receive logout method and terminate current session.k
    """
    # Logout the current session.
    auth.logout(request)
    # Redirect to login page after logout.
    return redirect('login')


@login_required
def index(request, userID):
    """ Instructor index url handler,
    receive request from success authentication
    return Instructor index page with all course
    listing course average score.
    """
    if request.method == 'GET':
        # Get current instructor identity.
        instructor = Instructor.objects.get(user__pk=userID)
        # Get courses.
        courseList = instructor.getCourses()
        # Initialize students list.
        studentList = []
        # For all students of the instructor,
        for student in instructor.getStudents():
            studentList.append(
                (
                    # record the student info,
                    student,
                    # the overall risk of the student,
                    "{:10.3f}".format(student.getOverallRisk()),
                    # and the average score of the student.
                    "{:10.3f}".format(student.getAverageGrade())
                )
            )
        # Sort students according to risk.
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        # Update course data
        for course in courseList:
            course.getCourseAverage()
        # Return rendered index page.
        return render(
            request,
            'presentation/index.html',
            {
                'userID': userID,
                # Pack the course list.
                'courseList': courseList,
                # Show top 5 students with high risks.
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
        # Get current instructor identity.
        instructor = Instructor.objects.get(user__pk=userID)
        # Get courses of the instructor.
        courseList = instructor.getCourses()
        # Update course data.
        for course in courseList:
            course.getCourseAverage()
        # Return rendered courses page.
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
        # Get current instructor identity.
        instructor = Instructor.objects.get(user__pk=userID)
        # Initialize student list.
        studentList = []
        # For all students of the instructor,
        for student in instructor.getStudents():
            studentList.append(
                (
                    # record the student info,
                    student,
                    # the overall risk of the student,
                    "{:10.3f}".format(student.getOverallRisk()),
                    # and the average score of the student.
                    "{:10.3f}".format(student.getAverageGrade())
                )
            )
        # Sort students by risks.
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        # Return rendered students page.
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
        # Get requested course.
        courseID = request.GET.get('courseID')
        course = Course.objects.get(id=courseID)
        # Update course data.
        course.getCourseAverage()
        # Initialize student list.
        studentList = []
        # For every student taking this course,
        for student in course.getStudents():
            studentList.append(
                (
                    # record the student info,
                    student,
                    # risk of the student in this course,
                    "{:10.3f}".format(student.getRiskFactor(course.name)),
                    # and grades of the student in this course
                    map(
                        lambda x: "{:10.3f}".format(x),
                        student.getGrade(course.name)
                    )
                )
            )
        # Sort students by risks.
        studentList.sort(key=(lambda x: x[1]), reverse=True)
        # Get visualization result image.
        imgURL = "/images/image_average_quiz_grade_course_"
        imgURL += course.name.replace(' ', '_') + ".png"
        # Return rendered course page.
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
        # Get requested student.
        studentID = request.GET.get('studentID')
        student = Student.objects.get(id=studentID)
        # Get requested course, if any.
        courseID = request.GET.get('courseID')
        if courseID is not None:
            # If a specific course is indicated.
            # Get the course entity.
            course = Course.objects.get(id=courseID)
            # Record risk of the student in this course.
            risk = "{:10.3f}".format(student.getRiskFactor(course.name))
            # Record grades of the student in this course.
            grades = map(
                lambda x: "{:10.3f}".format(x),
                student.getGrade(course.name)
            )
            # Get visualization result image.
            imgURL = "/images/image_quiz_student_"
            imgURL += course.name.replace(' ', '_') + "_"
            imgURL += student.name.replace(' ', '_') + ".png"
            # Ignore other variables.
            courseList = None
            avgRisk = None
            avgGrade = None
        else:
            # If no course is specified.
            # Record average risk of the student.
            avgRisk = "{:10.3f}".format(student.getOverallRisk())
            # Record average grade of the student.
            avgGrade = "{:10.3f}".format(student.getAverageGrade())
            # Initialize course list.
            courseList = []
            # For every course this student is taking,
            for course in student.getCourses():
                # Check if the course is related to the currently
                # login instructor.

                # Get current instructor identity
                instructor = Instructor.objects.get(user__pk=userID)
                # Check
                if course not in instructor.getCourses():
                    disabled = True
                else:
                    disabled = False
                # Get visualization result image.
                cImgURL = "/images/image_quiz_student_"
                cImgURL += course.name.replace(' ', '_') + "_"
                cImgURL += student.name.replace(' ', '_') + ".png"
                courseList.append(
                    (
                        # Record the course info,
                        course,
                        # whether the course is related to the instructor,
                        disabled,
                        # risk of the student in this course,
                        "{:10.3f}".format(student.getRiskFactor(course.name)),
                        # grades of the student in this course.
                        map(
                            lambda x: "{:10.3f}".format(x),
                            student.getGrade(course.name)
                        ),
                        # and the related image.
                        cImgURL
                    )
                )
            # Sort courses by risks.
            courseList.sort(key=(lambda x: x[2]), reverse=True)
            # Ignore other variables.
            course = None
            risk = None
            grades = None
            imgURL = None
        # Return rendered student page.
        return render(
            request,
            'presentation/student.html',
            {
                'userID': userID, 'student': student, 'imgURL': imgURL,
                'course': course, 'courseList': courseList, 'avgRisk': avgRisk,
                'avgGrade': avgGrade, 'risk': risk, 'grades': grades
            }
        )
