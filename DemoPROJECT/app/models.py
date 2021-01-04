from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=30)
    occupation = models.CharField(max_length=30)