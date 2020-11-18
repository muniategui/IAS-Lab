from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.forms import BookForm
from books.models import Book
from django.conf.urls import include, url
from django.views.static import serve
from django.conf import settings
from django.http import FileResponse
from books.models import Book
from books.classes import encrypter2
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.conf import settings
import io
# Create your views here.
@login_required
def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {'books':books})

@login_required
def upload(request):
    if(not request.user.uploader and not request.user.is_superuser):
        return redirect(home)
    form = BookForm()
    if request.method == "POST":
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,"uploadSuccess.html")
    return render(request, "upload.html",{'form':form})


@login_required
def delete(request):
    if (not request.user.is_superuser):
        return redirect(home)
    if request.method == "POST":
        Book.objects.get(id=request.POST['bookID']).delete()
    return redirect(home)


@login_required
def protected_serve(request, path, name, document_root=None):
    if path == 'Books':
        obj = get_object_or_404(Book, file=path+'/'+name)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=bytes(settings.SALT.encode("utf-8")),
            iterations=100000)

        key = base64.urlsafe_b64encode(kdf.derive(bytes(settings.SECRET_KEY_FILES.encode("utf-8"))))
        f = Fernet(key)
        stream = io.BytesIO(f.decrypt(open(document_root+'//'+path+'//'+name, 'rb').read()))
        return FileResponse(stream, as_attachment=False, filename=obj.OriginalName)
    if path == 'user_graph.png':
        if (not request.user.is_superuser):
            return redirect(home)
        return FileResponse(open(document_root+'//'+path,'rb'),as_attachment=False)
