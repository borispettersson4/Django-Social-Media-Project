# Generated by Django 2.1.5 on 2019-01-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190117_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
        migrations.AddField(
            model_name='sociallist',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='users.Profile'),
        ),
        migrations.AddField(
            model_name='sociallist',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to='users.Profile'),
        ),
    ]