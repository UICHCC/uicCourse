from django.db import models
from course.models import Course
from django.contrib.auth.models import User

# Create your models here.


class QuickVotes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    vote_status = models.NullBooleanField(blank=True, null=True)  # null = not vote, True = up vote, False = down vote
    is_invalid_vote = models.BooleanField(default=False)

    def __str__(self):
        return "%s vote course: %s" % (self.voter.username, self.course.course_name_en)
