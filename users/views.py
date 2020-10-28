from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm

def home(request):
    # If loged in return home
    if request.user.is_authenticated:
        return render(request, "home.html")
    # Redirect to login if not loged in
    return redirect('/login')

def register(request):
    # Create the register form
    form = UserCreationForm()
    if request.method == "POST":
        # Add the data received in post
        form = UserCreationForm(data=request.POST)
        # Validate
        if form.is_valid():

            # Create new user
            user = form.save()

            # If user created correctly
            if user is not None:
                # Login
                do_login(request, user)
                # Redirect
                return redirect('/')

    # If not post render register
    return render(request, "register.html", {'form': form})

def login(request):
    # Create empty login form
    LoginForm = AuthenticationForm()
    if request.method == "POST":
        # Add the data received in post
        form = AuthenticationForm(data=request.POST)
        # If valid form
        if form.is_valid():
            # Retrieve credentials
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verify user
            user = authenticate(username=username, password=password)

            # If user exists
            if user is not None:
                # Login
                do_login(request, user)
                # Go Home
                return redirect('/')

    # If not post render the login form
    return render(request, "login.html", {'form': LoginForm})

def logout(request):
    # End the session
    do_logout(request)
    # Redirect to root
    return redirect('/')