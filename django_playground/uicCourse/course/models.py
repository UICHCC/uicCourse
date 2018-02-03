from django.db import models


class Course(models.Model):
    course_name_en = models.TextField(null=True)
    course_name_cn = models.TextField(null=True)
    course_code = models.CharField(max_length=32, default='EMPTY_COURSE_CODE')
    course_units = models.IntegerField()
    course_class = models.CharField(max_length=32, default='DEFAULT_CLASS')
    course_descriptions = models.TextField(null=True)

    def __str__(self):
        return self.course_name_en


class InvitationCode(models.Model):
    invitation_code = models.TextField(null=True, unique=True)
    usability = models.BooleanField(default=True)

    def __str__(self):
        return self.invitation_code
