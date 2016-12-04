from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from ..models import Course, Instructor, Student
from django.contrib.auth.models import User
from . import course_view


def login(request):
    if request.method == 'GET':
        return render_to_response('presentation/login.html')
    # get or post are determined later:
    username = request.POST['username']
    password = request.POST['password']

    #####

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)

        if user.groups.filter(name='Instructor').exists():
            return course_view.index(request)
    else:
        return render_to_response('login.html')
