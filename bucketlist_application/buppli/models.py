from django.db import models

# Create your models here.


class BucketList(models.Model):

    name = models.CharField(max_length=100, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='bucketlists')

    class Meta:
        ordering = ('date_created',)
