from django import forms
from django.contrib.auth.forms import UserCreationForm

from videos.custom_auth.models import ApplicationUser


class UserRegister(UserCreationForm):
    class Meta:
        model = ApplicationUser
        fields = ('email', 'password1', 'password2')


class UserLogin(UserCreationForm):
    class Meta:
        model = ApplicationUser
        fields = ('email', 'password')

    # def super(UserRegister, self).save(commit=False):




