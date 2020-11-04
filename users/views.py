from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth.decorators import login_required
from users.forms import AuthenticationFormExtended
from users.forms import UserCreationFormExtended
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.db.models import Q

@login_required
def home(request):
    return render(request, "home.html")

def register(request):
    # Create the register form
    form = UserCreationFormExtended()
    if request.method == "POST":
        # Add the data received in post
        form = UserCreationFormExtended(data=request.POST)
        # Validate
        if form.is_valid():

            # Create new user
            user = form.save()

            # If user created correctly
            if user is not None:
                # Login
                do_login(request, user, backend='axes.backends.AxesBackend')
                # Redirect
                return redirect(home)

    # If not post render register
    return render(request, "register.html", {'form': form})

def login(request):
    # Create empty login form
    form = AuthenticationFormExtended()
    if request.method == "POST":
        # Add the data received in post
        form = AuthenticationFormExtended(request=request,data=request.POST)
        # If valid form
        if form.is_valid():
            # Retrieve credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verify user
            user = authenticate(request=request,username=username, password=password)

            # If user exists
            if user is not None:
                # Login
                do_login(request, user, backend='axes.backends.AxesBackend')
                # Go Home
                return redirect(home)

    # If not post render the login form
    return render(request, "login.html", {'form': form})

def logout(request):
    # End the session
    do_logout(request)
    # Redirect to root
    return redirect(login)

@login_required
def profile(request):
    print(request.user)
    invitedBy = User.objects.filter(Q(uuidNormal=request.user.invite) | Q(uuidAdmin =request.user.invite)).first()
    return render(request, "profile.html",{'invitedBy':invitedBy})