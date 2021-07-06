from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # by default it has argument required=True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# model form will allow us to create a form that will work with a specific DB model, we need one that updates the
# user model
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# this will allow us to update the image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
