from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(default = 'anonymous', max_length = 20)
    image = models.ImageField(default = 'default_profile.jpg', upload_to='profile_pics')
    badge = models.CharField(default = 'A', max_length = 1)
    following = models.ManyToManyField("self", related_name='followers', blank=True,  symmetrical=False)
    friends = models.ManyToManyField("self", related_name='friends', blank=True, symmetrical=True)
    date_active = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return(f'{self.user.username} Profile')

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.image.path)
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
    about = models.CharField(default = 'Write about yourself.', max_length = 160)
    quote = models.CharField(default = 'Write an original idea!', max_length = 80)
    #birthday = models.CharField(default = 'Write an original idea!', max_length = 80)
    #location = models.CharField(default = 'Write an original idea!', max_length = 80)
    #To be continued...

    def __str__(self):
        return(f'{self.user.username} Profile')

    def save(self, **kwargs):
        super().save()
        #Resize Images upon Profile creation
        img = Image.open(self.coverImage.path)
        if (img.height != 500 or img.width != 1200):
            output_size = (500,1200)
            img.thumbnail(output_size)
            img.save(self.coverImage.path)

    #This is an activity post item that can be a like, post, or comment



# Create your models here.
