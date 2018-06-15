from django.db import models

# Create your models here.


class Notice(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(default='')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.publish_date

    class Meta:
        ordering = ['-update_time']
