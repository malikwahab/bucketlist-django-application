from django.db import models

# Create your models here.


class BaseModel(models.Model):

    name = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_modified',)
        abstract = True


class BucketList(BaseModel):

    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='bucketlists')


class BucketListItem(BaseModel):

    done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(BucketList, related_name="items")
