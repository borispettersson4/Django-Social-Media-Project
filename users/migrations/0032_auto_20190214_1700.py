# Generated by Django 2.1.5 on 2019-02-14 21:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0031_auto_20190214_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='image',
            field=models.ImageField(default='default_profile.jpg', upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='group',
            name='mods',
            field=models.ManyToManyField(blank=True, related_name='mods', to=settings.AUTH_USER_MODEL),
        ),
    ]
