from django.shortcuts import render, redirect
from . models import TodayYesterdayUpdate, Organization
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date
from . form import TaskUpDateForm

today = date.today()

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
def task_view(request, date=None):
    user = request.user
    orgs = Organization.objects.all()
    organization = Organization
    for org in orgs:
        if user in org.users.all():
            organization = org
            break
    tasks = TodayYesterdayUpdate.objects.filter(organization=organization,
        date=today)

    # if there is not data for today data will created for requested user
    # if data created for today then data will be updated for requested user
    own_data = TodayYesterdayUpdate.objects.filter(organization=organization,
        date=today, user=request.user)
    if own_data:
        return render(request, 'task.html', {"tasks":tasks, "data":own_data[0]})
    return render(request, 'task.html', {"tasks":tasks, "data":own_data})


@login_required(login_url='/')
def create_task(request, pk=None):
    organization = Organization.objects.all()[0]
    if request.method == "GET":
        if pk is not None:
            try:
                data = TodayYesterdayUpdate.objects.get(id=pk)
                if data.user == request.user:
                    form = TaskUpDateForm(instance=data)
                    return render(request, 'taskform.html', {"form":form, "pk":pk})
                return HttpResponse("You are not authorised for this link")
            except:
                return HttpResponse("Something went wrong!!")

        # if user already created task but hit by url create task link
        if TodayYesterdayUpdate.objects.filter(organization=organization,
            date=today, user=request.user):
            return HttpResponse("you are already created task")
        form = TaskUpDateForm()
        return render(request, 'taskform.html', {"form":form})

    if request.method == "POST":
        if pk is not None:
            data = TodayYesterdayUpdate.objects.get(id=pk)
            form = TaskUpDateForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                return redirect('/task/')
        form = TaskUpDateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.organization = organization
            post.save()
            return redirect('/task/')
    return HttpResponse("Invalid form!! Try Again")
