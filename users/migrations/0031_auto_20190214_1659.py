# Generated by Django 2.1.5 on 2019-02-14 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20190214_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='image',
        ),
        migrations.RemoveField(
            model_name='group',
            name='mods',
        ),
        migrations.RemoveField(
            model_name='group',
            name='name',
        ),
        migrations.RemoveField(
            model_name='group',
            name='nick',
        ),
        migrations.RemoveField(
            model_name='group',
            name='owner',
        ),
    ]
