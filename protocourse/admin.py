from django.contrib import admin

# Register your models here.
from . import models
# Register your models here.
admin.site.register(models.Module)

admin.site.register(models.Workload)
