from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Discussions(models.Model):
    queId = models.AutoField(primary_key=True)
    catId = models.IntegerField()
    queTitle = models.CharField( max_length=255)
    queDesc = models.TextField()
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(default = now)

    def __str__(self):
        return self.queTitle + " by " + str(self.username)

class Comments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    queId = models.IntegerField()
    timestamp = models.DateTimeField(default = now)