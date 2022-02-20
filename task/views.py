from django.shortcuts import render, redirect
from . models import TodayYesterdayUpdate, Organization
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/task/')
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        u = authenticate(request, username=username, password=password)
        if u is not None:
            login(request, u)
            return redirect('/task/')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')

@login_required(login_url='/')
def task_view(request):
    user = request.user
    orgs = Organization.objects.all()
    organization = Organization
    for org in orgs:
        if user in org.users.all():
            organization = org
            break
    tasks = TodayYesterdayUpdate.objects.filter(organization=organization)
    return render(request, 'task.html', {'tasks': tasks})
