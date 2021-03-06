from django.db import models

# Create your models here.


class F2(models.Model):
    foreign_model = models.ForeignKey("ForeignModel", on_delete=models.CASCADE)

    def __str__(self):
        return "f2 model"


class ForeignModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TestModel(models.Model):
    int_field = models.IntegerField()
    char_field = models.CharField(max_length=100)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    f_field = models.ForeignKey(ForeignModel, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="Привет")

    def __str__(self):
        return "testModel"
