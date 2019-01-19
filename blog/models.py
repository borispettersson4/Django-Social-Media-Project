from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from PIL import Image
from .models import *

class Topic(models.Model):
    title = models.CharField(max_length = 20)
    def __str__(self):
        return (self.title)

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

class Post(models.Model):
    title = models.CharField(max_length = 100)
    image = models.ImageField(default = 'default.jpg', upload_to='post_pics')
    content = models.TextField(max_length = 500)
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    topics = models.ManyToManyField(Topic, blank=True, symmetrical=False)

    def __str__(self):
        return (self.title)

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

    def save(self):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
        if (img.height > 1920 or img.width > 1080):
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

    def save(self):
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
