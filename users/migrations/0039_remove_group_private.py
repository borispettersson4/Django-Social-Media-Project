# Generated by Django 2.1.5 on 2019-02-21 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_auto_20190221_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='private',
        ),
    ]