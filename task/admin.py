from django.contrib import admin
from . models import TodayYesterdayUpdate, Organization
# Register your models here.

admin.site.register([TodayYesterdayUpdate, Organization])
