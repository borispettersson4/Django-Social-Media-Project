from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
        "image": "Profile Image"
        }
        help_texts = {
        "image": ('Image will automatically be resized to 500 x 500 pixels.'),
        }

class ProfileSettingsUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileSettings
        fields = ['coverImage', 'quote', 'about']
        labels = {
        "coverImage": "Cover Image"
        }
        help_texts = {
        "coverImage": ('Image will automatically be resized to 1500 x 300 pixels.'),
        "about": ('Write about yourself! Whatever describes you. ( 160 characters or less. )'),
        "quote": ('What is your current original idea? ( 80 characters or less. )'),
        }

class ProfileNickUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick']
        labels = {
        "nick": "Display Name"
        }
        help_texts = {
            'nick': ('This is your primary display name. ( 20 characters or less. )'),
        }
