from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Country(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    code_exp = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'


class Project(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=510, blank=True, null=True)
    address = models.CharField(max_length=510, blank=True, null=True)
    started = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(blank=True, null=True, default=0)
    lng = models.FloatField(blank=True, null=True, default=0)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    archived = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'project'