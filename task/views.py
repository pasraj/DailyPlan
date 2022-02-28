from django.shortcuts import render, redirect
from . models import TodayYesterdayUpdate, Organization
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from . form import TaskUpDateForm, SignUpForm

# date object to string format
def dateString(date):
    return date.strftime("%d-%m-%Y")

# string date to date object
def strToDate(date):
    print("In function")
    print(date)
    return datetime.strptime(date, '%d-%m-%Y').date()

def is_same(date1, date2):
    return date1==date2

today = date.today()


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'signup.html', {"form":form})
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Done")
        else:
            return HttpResponse("Form is not valid")


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
    if date is not None:
        print("In task function")
        print("None date", date)
        currentDate = strToDate(date)
    else:
        currentDate = today
    yesterday = currentDate - timedelta(days=1)
    tomorrow = currentDate + timedelta(days=1)
    user = request.user

    # temporary based organization code
    orgs = Organization.objects.all()
    organization = Organization
    for org in orgs:
        if user in org.users.all():
            organization = org
            break
        else:
            return HttpResponse("you are not belong to any organization")
    tasks = TodayYesterdayUpdate.objects.filter(organization=organization,
    date=currentDate)
    # if there is not data for today data will created for requested user
    # if data created for today then data will be updated for requested user
    own_data = TodayYesterdayUpdate.objects.filter(organization=organization,
        date=currentDate, user=request.user)

    if own_data:
        context = {
            "tasks":tasks,
            "previous_day": dateString(yesterday),
            "next_day": dateString(tomorrow),
            "is_same_day": is_same(currentDate, today),
            "currentDate": currentDate,
            "data":own_data[0]
            }
        return render(request, 'task.html',context )
    context = {
            "tasks":tasks,
            "previous_day": dateString(yesterday),
            "currentDate": currentDate,
            "next_day": dateString(tomorrow),
            "is_same_day": is_same(currentDate, today),
            "data":own_data
            }
    return render(request, 'task.html', context)


@login_required(login_url='/')
def create_task(request, pk=None):

    # temporary based organization code
    orgs = Organization.objects.all()
    organization = Organization
    for org in orgs:
        if request.user in org.users.all():
            organization = org
            break

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
