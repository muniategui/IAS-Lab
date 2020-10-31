from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class AuthenticationFormExtended(AuthenticationForm):
    captcha = CaptchaField()

class UserCreationFormExtended(UserCreationForm):
    captcha = CaptchaField()