from django.db import models
from django.utils.translation import gettext_lazy as _


class Division(models.Model):
    division_en = models.CharField(max_length=128, verbose_name='Division English Title')
    division_cn = models.CharField(max_length=128, verbose_name='Division Chinese Title')
    division_en_abbr = models.CharField(max_length=128, verbose_name='Abbreviation for Division\'s English Title')

    class Meta:
        verbose_name = _('division')
        verbose_name_plural = _('divisions')

    def __str__(self):
        return "%s (%s)" % (self.division_en, self.division_en_abbr)


class Major(models.Model):
    major_en = models.CharField(max_length=128, verbose_name='Major English Title')
    major_cn = models.CharField(max_length=128, verbose_name='Major Chinese Title')
    major_en_abbr = models.CharField(max_length=128, verbose_name='Abbreviation for Major\'s English Title')

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
    name = models.CharField(max_length=128, verbose_name='Type Name')
    name_abbr = models.CharField(max_length=128, verbose_name='Type Abbreviation')

    def __str__(self):
        return self.name_abbr


class Course(models.Model):
    course_id = models.CharField(max_length=32, default='NULL0000', verbose_name='Course Code')
    course_name_en = models.CharField(max_length=128, verbose_name='Course English Name')
    course_name_cn = models.CharField(max_length=128, verbose_name='Course Chinese Name')
    course_units = models.IntegerField(default=3, verbose_name='Course Credit', help_text='3 Units or 1 Unit')
    course_description = models.TextField(default='', verbose_name='Course Description')
    course_pre_request = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,
                                           verbose_name='Course Pre-Request')
    course_type = models.ForeignKey(CourseType, null=True, on_delete=models.CASCADE, verbose_name='Course Type')
    course_major_take = models.ManyToManyField(ValidDivisionMajorPair, verbose_name='Major(s) that take this course')
    is_visible = models.BooleanField(default=True, verbose_name='Visibility of the course')
    is_rateable = models.BooleanField(default=True, verbose_name='Rate-ability of the course')
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.course_name_en, self.course_id)
