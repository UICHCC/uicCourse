from django import forms
from . import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'
        exclude = ['up_vote', 'down_vote', 'update_time', 'view_times']
