# Generated by Django 2.1.5 on 2019-01-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_sociallist'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='badge',
            field=models.CharField(default='A', max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='nick',
            field=models.CharField(default='anonymous', max_length=20),
        ),
        migrations.AddField(
            model_name='sociallist',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='users.SocialList'),
        ),
        migrations.AddField(
            model_name='sociallist',
            name='friends',
            field=models.ManyToManyField(related_name='_sociallist_friends_+', to='users.SocialList'),
        ),
    ]
