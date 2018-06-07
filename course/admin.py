from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Division)

admin.site.register(models.Major)

admin.site.register(models.ValidDivisionMajorPair)