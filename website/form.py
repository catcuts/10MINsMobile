from django import forms
from django.core.exceptions import ValidationError
from  django.contrib.auth.password_validation import validate_password

class ProfileForm(forms.Form):
    username = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder': '你的真实姓名'}))

    password = forms.CharField(required=False, widget=forms.PasswordInput(), validators=[validate_password])


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
