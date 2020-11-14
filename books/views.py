from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.forms import BookForm
from books.models import Book
from django.conf.urls import include, url
from django.views.static import serve
from django.conf import settings

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
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)
