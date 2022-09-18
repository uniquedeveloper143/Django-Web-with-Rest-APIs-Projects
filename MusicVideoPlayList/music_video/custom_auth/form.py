from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from music_video.custom_auth.models import ApplicationUser


class UserRegister(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(required=True)

    class Meta:
        model = ApplicationUser
        fields = ('name', 'email', 'phone', 'password1', 'password2')

    # def __init__(self, *args, **kwargs):
    #     super(UserRegister, self).__init__(*args, **kwargs)
    #     self.fields['name'].required = True


class UserLogin(UserCreationForm):
    class Meta:
        model = ApplicationUser
        fields = ('email', 'password')
