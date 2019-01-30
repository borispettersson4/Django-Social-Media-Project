# Generated by Django 2.1.5 on 2019-01-17 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190117_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(default='self', related_name='followers', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(default='self', related_name='_profile_friends_+', to='users.Profile'),
        ),
    ]