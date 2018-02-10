from django.db import models
from django.contrib.auth.models import User


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


class Comments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_recommend = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    pid = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['up_vote', '-pub_date']

    def __str__(self):
        return str(self.id)
