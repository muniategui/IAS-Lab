from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.core.exceptions import ValidationError
import uuid
from django.forms import ModelForm
from books.models import Book



class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['OriginalName']
        widgets = {
             'year': forms.TextInput(),
             'pages': forms.TextInput(),
        }
