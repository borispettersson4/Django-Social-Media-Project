# Generated by Django 2.1.5 on 2019-02-04 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
    ]