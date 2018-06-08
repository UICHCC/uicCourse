from django.db import models
from django.utils.translation import gettext_lazy as _


class Division(models.Model):
    division_en = models.CharField(max_length=128, null=True)
    division_cn = models.CharField(max_length=128, null=True)
    division_en_abbr = models.CharField(max_length=128, null=True)

    class Meta:
        verbose_name = _('division')
        verbose_name_plural = _('divisions')

    def __str__(self):
        return "%s (%s)" % (self.division_en, self.division_en_abbr)


class Major(models.Model):
    major_en = models.CharField(max_length=128, null=True)
    major_cn = models.CharField(max_length=128, null=True)
    major_en_abbr = models.CharField(max_length=128, null=True)

    class Meta:
        verbose_name = _('major')
        verbose_name_plural = _('majors')

    def __str__(self):
        return "%s (%s)" % (self.major_en, self.major_en_abbr)


class ValidDivisionMajorPair(models.Model):
    major = models.OneToOneField(Major, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return "%s @ %s" % (self.major.major_en, self.division.division_en)


class CourseType(models.Model):
    name = models.CharField(max_length=128, null=True)
    name_abbr = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name_abbr


class Course(models.Model):
    course_id = models.CharField(max_length=32, default='NULL0000')
    course_name_en = models.CharField(max_length=128, null=True)
    course_name_cn = models.CharField(max_length=128, null=True)
    course_units = models.IntegerField(default=3)
    course_description = models.TextField(null=True)
    course_pre_request = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    course_type = models.ForeignKey(CourseType, default=0, on_delete=models.CASCADE)
    course_major_take = models.ManyToManyField(ValidDivisionMajorPair)
    is_visible = models.BooleanField(default=True)
    is_rateable = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.course_name_en, self.course_id)
