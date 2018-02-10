from django.contrib import admin

from . import models

admin.site.register(models.Course)

admin.site.register(models.InvitationCode)

admin.site.register(models.Comments)