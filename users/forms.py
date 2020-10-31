from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.core.exceptions import ValidationError
import uuid

class AuthenticationFormExtended(AuthenticationForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ["username", "password"]
class UserCreationFormExtended(UserCreationForm):
    captcha = CaptchaField()
    email2 = forms.EmailField(label='Email Confirmation')
    invite = forms.CharField(max_length=256)
    class Meta:
        model = User
        fields = ["username", "email" ,"email2" ,"password1", "password2", "invite"]

    def clean_invite(self):
        uuidInvite = self.cleaned_data['invite']
        if (User.objects.filter(uuidNormal=uuidInvite).exists() or User.objects.filter(uuidAdmin=uuidInvite).exists()):
            return uuidInvite
        raise ValidationError("Invalid invitation")
    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email and email2 and email != email2:
            raise ValidationError("Emails do not match")
        return email2