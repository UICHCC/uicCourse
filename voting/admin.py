from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.QuickVotes)

admin.site.register(models.Tags)

admin.site.register(models.UserTaggingCourse)