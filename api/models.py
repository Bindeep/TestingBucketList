from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BucketList(models.Model):
    owner = models.ForeignKey(User, related_name='bucketLists', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
