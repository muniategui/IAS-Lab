from django.db import models

class Book(models.Model):
    Title = models.CharField(max_length=512, blank=False)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)