from django.db import models

# Create your models here.


class TestModel(models.Model):
    i = models.IntegerField()
    c = models.CharField(max_length=255)
    d = models.DateField()
    dt = models.DateTimeField()
