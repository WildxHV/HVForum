from django.db import models

# Create your models here.
class Categories(models.Model):
    catId = models.AutoField(primary_key=True)
    title = models.CharField( max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title