from django.db import models
from course.models import Course
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.


class Workload(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    lecture_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                       verbose_name="Lecture workload", validators=[MinValueValidator(0.0)])
    tutorial_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                        verbose_name="Tutorial workload", validators=[MinValueValidator(0.0)])
    project_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                       verbose_name="Project workload", validators=[MinValueValidator(0.0)])
    preparation_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                           verbose_name="Preparation workload", validators=[MinValueValidator(0.0)])
    lab_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                   verbose_name="Lab workload", validators=[MinValueValidator(0.0)])
    homework_time = models.DecimalField(default=0, max_digits=3, decimal_places=1,
                                        verbose_name="Homework workload", validators=[MinValueValidator(0.0)])

    def __str__(self):
        return "Estimate workload for %s, %s hrs" % (self.course.course_id, (self.lecture_time +
                                                                           self.tutorial_time +
                                                                           self.project_time +
                                                                           self.preparation_time +
                                                                           self.lab_time +
                                                                           self.homework_time))

    class Meta:
        verbose_name = _('course workload')
        verbose_name_plural = _('course workload')


class Module(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    quiz = models.BooleanField(default=False)
    assignment = models.BooleanField(default=False)
    essay = models.BooleanField(default=False)
    project = models.BooleanField(default=False)
    attendance = models.BooleanField(default=False)
    reading_material = models.BooleanField(default=False)
    presentation = models.BooleanField(default=False)
    mid_term_Exam = models.BooleanField(default=False)
    final_exam = models.BooleanField(default=False)
    feedback_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s module (update time: %s)" % (self.course.course_id, self.update_time)

    class Meta:
        verbose_name = _('course module')
        verbose_name_plural = _('course module')
