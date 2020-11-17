from django.db import models
from books.validators import validate_pdf
from django.conf import settings
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import io
class Book(models.Model):
    title = models.CharField(max_length=512)
    author = models.CharField(max_length=512, blank=True)
    isbn10 = models.CharField(max_length=10, blank=True)
    isbn13 = models.CharField(max_length=13, blank=True)
    year = models.IntegerField(blank=True,null=True)
    pages = models.IntegerField(blank=True,null=True)
    language = models.CharField(max_length=64,blank=True)
    file = models.FileField(upload_to='Books/', max_length=256,validators=[validate_pdf])
    OriginalName = models.CharField(max_length=256,blank=True)

    def save(self, *args, **kwargs):
        
        self.OriginalName=self.file.name

        kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = bytes(settings.SALT.encode("utf-8")),
        iterations = 100000)

        key = base64.urlsafe_b64encode(kdf.derive(bytes(settings.SECRET_KEY_FILES.encode("utf-8"))))
        f = Fernet(key)
        self.file.seek(0)
        out = io.BytesIO(f.encrypt(self.file.read()))
        self.file.file.file=out
        super(Book, self).save(*args, **kwargs)


