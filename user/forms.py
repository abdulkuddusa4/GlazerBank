from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user.models import Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class ProfileCreationForm(forms.ModelForm):
    user_account = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Profile
        fields = ['user_account', 'profile_image', 'nid', 'passport', 'driver_license']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)