from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from PIL import Image
from .models import *
from users.models import *

class Topic(models.Model):
    title = models.CharField(max_length = 20)
    date_posted = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return (self.title)

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

class Post(models.Model):
    title = models.CharField(max_length = 100,blank=True)
    image = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    video = models.FileField(upload_to='video_files', null=True, verbose_name="Video", blank=True)
    audio = models.FileField(upload_to='audio_files', null=True, verbose_name="Audio", blank=True)
    content = models.TextField(max_length = 500, blank=True)
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    topics = models.ManyToManyField(Topic, blank=True, symmetrical=False)
    people = models.ManyToManyField(User, blank=True,related_name='people', symmetrical=False)
    reply = models.ForeignKey("self", on_delete = models.CASCADE, blank=True, default = "self", null=True)
    repost = models.ForeignKey("self", on_delete = models.CASCADE,related_name='reposts', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True)
    link = models.CharField(max_length = 150,blank=True)

    def __str__(self):
        return (f'{self.author} : {self.content}')

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

    def cast_empty_reference(self):
        self.reply = self
        super().save()



    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1920 and img.width > 1080):
            output_size = (1080,720)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Message(models.Model):
    image = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    video = models.FileField(upload_to='video_files', null=True, verbose_name="Video", blank=True)
    audio = models.FileField(upload_to='audio_files', null=True, verbose_name="Audio", blank=True)
    content = models.TextField(max_length = 500, blank=True)
    date_posted = models.DateTimeField(default = timezone.now)
    recepient = models.ForeignKey(User, on_delete = models.CASCADE,related_name='msgrecepient', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name='msgsender', blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True, symmetrical=False)
    people = models.ManyToManyField(User, blank=True, symmetrical=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return (f'Message From {self.sender} : To {self.recepient}')

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

    def cast_empty_reference(self):
        self.reply = self
        super().save()

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1920 and img.width > 1080):
            output_size = (1080,720)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    content = models.TextField(max_length = 500)
    date_posted = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return (f"Re: {self.post.title}")

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1920 or img.width > 1080):
            output_size = (1080,720)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def create_self(self, author, post, image, content):
        obj = self.create(author=author, post=post, image=image, content=content)
        return obj

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return (f"{self.post.title}")

class Activity(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, default=None)
    date = models.DateTimeField(default = timezone.now)
    type = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return (f"{self.author}")

class Notification(models.Model):
    recepient = models.ForeignKey(User, on_delete = models.CASCADE,related_name='recepient', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name='sender', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, default=None,blank=True, null=True)
    type = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    first_seen = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default = timezone.now)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return (f"To {self.recepient} From {self.sender}")

    def save(self, **kwargs):
        super().save()


class Request(models.Model):
    recepient = models.ForeignKey(User, on_delete = models.CASCADE,related_name='requestant', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name='requester', blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default = timezone.now)
    type = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return (f"To {self.recepient} From {self.sender}")

    def save(self, **kwargs):
        super().save()

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, default=None,blank=True, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default = timezone.now)

    choice_1 = '1'
    choice_2 = '2'
    choice_3 = '3'
    choice_4 = '4'
    choice_5 = '5'
    CHOICES = (
        (choice_1,'Offensive/Abusive Material'),
        (choice_2,'Illicit Material'),
        (choice_3,'Personal Threats'),
        (choice_4,'Security Concern'),
        (choice_5,'Spam'),
    )
    report_choice = models.CharField(max_length=1,choices=CHOICES)
    comment = models.CharField(max_length = 300, blank=True)

    def __str__(self):
        return (f"Report From {self.author} to {self.post.author} at post : {self.post.id}")

    def save(self, **kwargs):
        super().save()
