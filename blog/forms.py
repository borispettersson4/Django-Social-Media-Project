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

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_choice', 'comment']
        labels = {
        "report_choice": "What Does This Post Contain?",
        "comment" : "Additional Information"
        }
        help_texts = {
        "coverImage": ('Image will automatically be resized to 1500 x 300 pixels.'),
        "about": ('Write about yourself! Whatever describes you. ( 160 characters or less. )'),
        "quote": ('What is your current original idea? ( 80 characters or less. )'),
        }

class NewImage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']
