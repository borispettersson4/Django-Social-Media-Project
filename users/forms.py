from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NameRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick']
        labels = {
        "nick": "Display Name"
        }
        help_texts = {
        'nick': ('This is your primary display name. ( 20 characters or less. )'),
        }

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

class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','type','members','image']
        labels = {
        "image": "Group Image",
        "name": "Group Name",
        "members": "Group Members",
        "mods": "Group Moderators",
        "type": "Group Type"
        }
        help_texts = {
        "image": ('Image will automatically be resized to 500 x 500 pixels.'),
        "name": ('Name of your group. Must be unique.'),
        "members": ('Hold down "Control", or "Command" on a Mac, to select more than one.'),
        "mods": ('Hold down "Control", or "Command" on a Mac, to select more than one.'),
        "type": ("Once checked, only group members are able to see this group's content"),
        }

class GroupSettingsUpdateForm(forms.ModelForm):
    class Meta:
        model = GroupSettings
        fields = ['coverImage', 'quote', 'about']
        labels = {
        "coverImage": "Cover Image",
        "about": "Summary"
        }
        help_texts = {
        "coverImage": ('Image will automatically be resized to 1500 x 300 pixels.'),
        "about": ('Write about your group. What is it? ( 160 characters or less. )'),
        "quote": ('What is the group motto? ( 80 characters or less. )'),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['quality_speed','quality_features','quality_visual','quality_stability','quality_responsiveness','comment']
        labels = {
        "comment": "Additional Comments",
        "quality_speed": "What do you think of load times and overall performance?",
        "quality_features": "Do you feel like the available features are sufficient?",
        "quality_visual": "What do you think of the visual design of the application?",
        "quality_stability": "Does the application give you a stable and bug-free experience?",
        "quality_responsiveness": "Do you feel like you're getting relevant and important information?",
        }
        help_texts = {
        "comment": ('Additional commentary. What are your ideas to make the app better?'),
        "quality_speed": ('How long does it take for you to upload a post, like, comment, etc.'),
        "quality_features": ('Some features : posting, commenting, liking, video playback, profile editing, etc.'),
        "quality_visual": ('Example : comfortable colors and shapes, text readability, and visual clarity.'),
        "quality_stability": ('Does the application do anything out of the ordinary? Do buttons work as expected?'),
        "quality_responsiveness": ('Do notifications, activities, and posts give you information you care about?'),
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
