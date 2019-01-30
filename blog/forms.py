from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from bootstrap_modal_forms.mixins import *
from crispy_forms.layout import *

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','image']

class ViewPostForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class NewPostForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class NewImage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']
