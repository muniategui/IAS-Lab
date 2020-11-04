from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.forms import BookForm

# Create your views here.
@login_required
def home(request):
    return render(request, "home.html")

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