from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models

class User(AbstractUser):
    email = models.EmailField(max_length=256,blank=False)
    uuidNormal = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    uuidAdmin = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    invite = models.UUIDField('Invite',primary_key=False, null=True,blank=False)
    uploader = models.BooleanField(primary_key=False,default=True)

    def save(self, *args, **kwargs):
        if (User.objects.filter(uuidAdmin=self.invite).exists()):
            self.uploader = True

        while(User.objects.filter(uuidNormal=self.uuidAdmin).exists() or User.objects.filter(uuidAdmin=self.uuidNormal).exists()):
            self.uuidAdmin = uuid.uuid4()
            self.uuidNormal = uuid.uuid4()

        super(User, self).save(*args, **kwargs)
