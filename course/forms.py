from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id',
                  'course_name_en',
                  'course_name_cn',
                  'course_units',
                  'course_description',
                  'course_pre_request',
                  'course_type',
                  'course_major_take']
