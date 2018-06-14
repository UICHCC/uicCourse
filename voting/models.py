from django.db import models
from course.models import Course
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class QuickVotes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Voting Course')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Voter')
    vote_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    vote_status = models.NullBooleanField(blank=True, null=True)  # null = not vote, True = up vote, False = down vote
    is_invalid_vote = models.BooleanField(default=False)

    def __str__(self):
        return "%s vote course: %s" % (self.voter.username, self.course.course_name_en)

    class Meta:
        verbose_name = _('Quick Vote')
        verbose_name_plural = _('Quick Votes')


class Tags(models.Model):
    tag_title = models.CharField(max_length=128, unique=True, verbose_name='Tag Title')
    tag_description = models.TextField(default='', verbose_name='Tag Description')
    tag_opposite = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    tag_sentiment_index = models.FloatField(default=0, verbose_name='Tag Sentiment Index',
                                            help_text='Positive number for positive emotions; Negative number for negative emotions, 0 for neutral emotion')

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class UserTaggingCourse(models.Model):
    tag_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Tagging course',
                                   related_name='course_tags')
    tagger = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Course Tagger')
    tags = models.ManyToManyField(Tags, verbose_name='User\'s tag(s) for this course')
    tag_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s tag course: %s' % (self.tagger.username, self.tag_course.course_name_en)

    class Meta:
        verbose_name = _('User Review')
        verbose_name_plural = _('User Reviews')
