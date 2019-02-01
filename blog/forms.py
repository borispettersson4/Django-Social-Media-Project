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

class NewPostForm(forms.Form):
    image = forms.ImageField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(widget=forms.HiddenInput)
    media = forms.FileField(widget=forms.HiddenInput, required=False)
    tags = forms.CharField(widget=forms.HiddenInput, required=False)

class NewImage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']
