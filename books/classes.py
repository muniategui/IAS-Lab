import io
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.conf import settings
import builtins

class encrypter:
    def __init__(self, real_file):
        self.origOut = real_file

    def __getattr__(self, attr_name):  # provide everything a file has
        return getattr(self.origOut, attr_name)

    def read(self, size=-1):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes(settings.SALT.encode("utf-8")),
            iterations=100000)

        key = base64.urlsafe_b64encode(kdf.derive(bytes(settings.SECRET_KEY_FILES.encode("utf-8"))))
        f = Fernet(key)
        return f.decrypt(super().read())
class encrypter2(object):
    """A basic file-like object."""

    def __init__(self, path, *args, **kwargs):
        self._file = open(path, *args, **kwargs)

    def read(self, n_bytes = -1):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes(settings.SALT.encode("utf-8")),
            iterations=100000)

        key = base64.urlsafe_b64encode(kdf.derive(bytes(settings.SECRET_KEY_FILES.encode("utf-8"))))
        f = Fernet(key)
        return f.decrypt(self._file.read(n_bytes))

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, e_tb):
        self._file.close()
        self._file = None