from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=50)

class TodayYesterdayUpdate(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    today_update = models.TextField()
    yesterday_update = models.TextField()
    blocker = models.TextField()
    time = models.TimeField(default=now)
    date = models.DateField(default=now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
