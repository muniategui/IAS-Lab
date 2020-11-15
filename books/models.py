from django.db import models
from books.validators import validate_pdf

class Book(models.Model):
    title = models.CharField(max_length=512)
    author = models.CharField(max_length=512, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    year = models.IntegerField(blank=True,null=True)
    pages = models.IntegerField(blank=True,null=True)
    language = models.CharField(max_length=64,blank=True)
    file = models.FileField(upload_to='Books/', max_length=256,validators=[validate_pdf])

