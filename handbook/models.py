from django.db import models
from course.models import ValidDivisionMajorPair

# Create your models here.


class HandbookEntity(models.Model):
    title_en = models.CharField(max_length=128, verbose_name='Item English Title')
    title_cn = models.CharField(max_length=128, verbose_name='Item Chinese Title')
    unit = models.IntegerField(default=3, verbose_name='Item Credit', help_text='Unit for this item')
    major = models.ForeignKey(ValidDivisionMajorPair, on_delete=models.CASCADE)
    admission_year = models.PositiveSmallIntegerField(default=2005, verbose_name='Admission Year that item belongs')
    study_semester = models.PositiveSmallIntegerField(default=1, verbose_name='Semester of this item')
    comment = models.CharField(max_length=512, verbose_name='More info about this item', blank=True)
    is_course_category = models.BooleanField(default=False, verbose_name='Is this item a a course category')
    priority = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title_en

    class Meta:
        ordering = ['-admission_year', 'study_semester', 'priority']