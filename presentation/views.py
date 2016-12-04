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
