from django.forms import ModelForm
from . models import TodayYesterdayUpdate


class TaskUpDateForm(ModelForm):
    class Meta:
        model = TodayYesterdayUpdate
        fields = ['yesterday_update', 'today_update', 'blocker']
