from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from io import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(default = 'New User', max_length = 20)
    image = models.ImageField(default = 'default_profile.jpg', upload_to='profile_pics')
    badge = models.CharField(default = 'A', max_length = 1)
    following = models.ManyToManyField("self", related_name='followers', blank=True,  symmetrical=False)
    friends = models.ManyToManyField("self", related_name='friends', blank=True, symmetrical=True)
    date_active = models.DateTimeField(default = timezone.now)
    can_send_feedback = models.BooleanField(default=True)
    can_send_reports = models.BooleanField(default=True)

    def __str__(self):
        return(f'{self.user.username} Profile')

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1000 and img.width > 1000):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def defaultValues(self):
        self.nick = 'default'
        self.badge = 'd'
        super(Profile, self).save()

class ProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coverImage = models.ImageField(default = 'default_cover.png', upload_to='cover_pics')
    about = models.CharField(default = '', max_length = 160, blank=True)
    quote = models.CharField(default = '', max_length = 80, blank=True)
    #birthday = models.CharField(default = 'Write an original idea!', max_length = 80)
    #location = models.CharField(default = 'Write an original idea!', max_length = 80)
    #To be continued...

    def __str__(self):
        return(f'{self.user.username} Profile')

    def save(self, **kwargs):
        im = Image.open(self.coverImage)
        output = BytesIO()
        im = im.resize((1500,300))
        im.save(output, format='PNG', quality=100)
        output.seek(0)
        self.coverImage = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.coverImage.name.split('.')[0], 'image/png', sys.getsizeof(output), None)
        super(ProfileSettings,self).save()

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    nick = models.CharField(default = 'New Group', max_length = 20)
    image = models.ImageField(default = 'default_profile.jpg', upload_to='profile_pics')
    members = models.ManyToManyField(User, blank=True,related_name='members')
    followers = models.ManyToManyField(User, blank=True,related_name='followers')
    mods = models.ManyToManyField(User, blank=True,related_name='mods')
    date_active = models.DateTimeField(default = timezone.now)
    choice_1 = '1'
    choice_2 = '2'
    choice_3 = '3'
    choice_4 = '4'
    choice_5 = '5'
    CHOICES = (
        (choice_1,'Open'),
        (choice_2,'Public'),
        (choice_3,'Public Invite-Only'),
        (choice_4,'Private'),
        (choice_5,'Private Invite-Only'),
    )

    type = models.CharField(max_length=1,choices=CHOICES, default=choice_2)

    choice_1 = '1'
    choice_2 = '2'
    CHOICES = (
        (choice_1,'None'),
        (choice_2,'Hide Owner and Member Identities'),
    )

    anonymity = models.CharField(max_length=1,choices=CHOICES, default=choice_1)

    def __str__(self):
        return(f'{self.name} Group')

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1000 and img.width > 1000):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def defaultValues(self):
        self.nick = 'default'
        self.badge = 'd'
        super(Group, self).save()

class GroupSettings(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    coverImage = models.ImageField(default = 'default_cover.png', upload_to='cover_pics')
    about = models.CharField(default = '', max_length = 160, blank=True)
    quote = models.CharField(default = '', max_length = 80, blank=True)

    def __str__(self):
        return(f'{self.group.name} Group Settings')

    def save(self, **kwargs):
        im = Image.open(self.coverImage)
        output = BytesIO()
        im = im.resize((1500,300))
        im.save(output, format='PNG', quality=100)
        output.seek(0)
        self.coverImage = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.coverImage.name.split('.')[0], 'image/png', sys.getsizeof(output), None)
        super(GroupSettings,self).save()

class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default = timezone.now)

    choice_1 = 'A'
    choice_2 = 'B'
    choice_3 = 'C'
    choice_4 = 'D'
    choice_5 = 'F'
    CHOICES = (
        (choice_1,'Very Pleased'),
        (choice_2,'Pleased'),
        (choice_3,'Neutral'),
        (choice_4,'Needs Work'),
        (choice_5,'Unacceptable'),
    )
    quality_speed = models.CharField(max_length=1,choices=CHOICES)
    quality_features = models.CharField(max_length=1,choices=CHOICES)
    quality_visual = models.CharField(max_length=1,choices=CHOICES)
    quality_stability = models.CharField(max_length=1,choices=CHOICES)
    quality_responsiveness = models.CharField(max_length=1,choices=CHOICES)
    comment = models.CharField(max_length = 300, blank=True)

    def __str__(self):
        return (f"Feedback From {self.author}")

    def save(self, **kwargs):
        super().save()
