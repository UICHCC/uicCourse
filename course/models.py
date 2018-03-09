from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    UIC_DIVISION = (('DST', 'Division of Science and Technology'),
                    ('DBM', 'Division of Business and Management'),
                    ('DHSS', 'Division of Humanities and Social Sciences'),
                    ('DCC', 'Division of Culture and Creativity'),
                    ('ALL', 'All Division'))
    UIC_MAJOR = (
        ('DST', (
            ('FST', 'Food Science and Technology'),
            ('ENVS', 'Environmental Science'),
            ('APSY', 'Applied Psychology'),
            ('STAT', 'Statistics'),
            ('FM', 'Financial Mathematics'),
            ('CST', 'Computer Science and Technology'),
            ('DS', 'Data Science'),
            ('ALLDST', 'All DST Major')
        )),
        ('DBM', (
            ('ACCT', 'Accounting'),
            ('FIN', 'Finance'),
            ('AE', 'Applied Economics'),
            ('EBIS', 'e-Business Management and Information Systems'),
            ('MHR', 'Management of Human Resources'),
            ('MKT', 'Marketing Management'),
            ('EPIN', 'Entrepreneurship and Innovation'),
            ('ALLDBM', 'All DBM Major')
        )),
        ('DCC', (
            ('CCM', 'Culture, Creativity and Management'),
            ('CTV', 'Cinema and Television'),
            ('MAD', 'Media Arts and Design'),
            ('ALLDCC', 'All DCC Major')
        )),
        ('DHSS', (
            ('GIR', 'Government and International Relations'),
            ('SWSA', 'Social Work and Social Administration'),
            ('IJ', 'International Journalism'),
            ('PRA', 'Public Relations and Advertising'),
            ('ATS', 'Applied Translation Studies '),
            ('ELLS', 'English Language and Literature Studies'),
            ('ALLDHSS', 'All DHSS Major')
        )),
        ('ALL', 'ALL Major')
    )
    UIC_COURSE_CATEGORY = (
        ('BBAC', 'BBA (Hons) Core'),
        ('MR', 'Major Required'),
        ('ME', 'Major Elective'),
        ('GEC', 'General Education Core'),
        ('GED', 'General Education Distribution'),
        ('WPEX', 'Whole Person Education Experiential Learning Modules'),
        ('FE', 'Free Elective')
    )
    UIC_COURSE_UNITS = (
        (3, 'Three Units'),
        (1, 'One Unit')
    )
    course_name_en = models.CharField(max_length=128, null=True)
    course_name_cn = models.CharField(max_length=128, null=True)
    course_code = models.CharField(max_length=32, default='EMPY1003')
    course_units = models.IntegerField(default=3, choices=UIC_COURSE_UNITS)
    course_class = models.CharField(max_length=32, default='DEFAULT_CLASS')
    course_major = models.CharField(max_length=32, default='ALL', choices=UIC_MAJOR)
    course_division = models.CharField(max_length=32, default='ALL', choices=UIC_DIVISION)
    course_category = models.CharField(max_length=32, default='FE', choices=UIC_COURSE_CATEGORY)
    course_descriptions = models.TextField(null=True, default='To be added')
    course_pre_request = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING)
    up_vote = models.IntegerField(default=0)
    down_vote = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    view_times = models.IntegerField(default=0)
    is_display_score= models.BooleanField(default=True)

    def __str__(self):
        return self.course_name_en


class InvitationCode(models.Model):
    invitation_code = models.TextField(null=True, unique=True)
    usability = models.BooleanField(default=True)
    who_register = models.ForeignKey(User, on_delete=models.CASCADE)

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


class QuickVotes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    vote_status = models.NullBooleanField(blank=True, null=True)  # null = not vote, True = up vote, False = down vote
    is_invalid_vote = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Tags(models.Model):
    tag_name_en = models.CharField(max_length=128, null=True)
    tag_name_cn = models.CharField(max_length=128, null=True)
    tag_descriptions = models.TextField(null=True, default='To be added')
    tag_weighted = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.tag_name_en)
