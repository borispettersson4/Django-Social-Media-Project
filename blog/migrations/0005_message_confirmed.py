# Generated by Django 2.1.5 on 2019-03-01 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]