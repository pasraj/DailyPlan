from django.shortcuts import render
from . models import TodayYesterdayUpdate
# Create your views here.

def task_view(request):
    user = request.user
    orgs = Organization.objects.all()
    organization = Organization
    for org in orgs:
        if user in org.users.all():
            organization = org
            break
    tasks = TodayYesterdayUpdate.objects.filter(organization=organization)
    return HttpResponse(tasks)
