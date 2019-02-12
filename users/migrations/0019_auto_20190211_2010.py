# Generated by Django 2.1.5 on 2019-02-12 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20190211_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_send_reports',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='quality_features',
            field=models.CharField(choices=[('A', 'Very Pleased'), ('B', 'Pleased'), ('C', 'Neutral'), ('D', 'Needs Work'), ('F', 'Unacceptable')], max_length=1),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='quality_responsiveness',
            field=models.CharField(choices=[('A', 'Very Pleased'), ('B', 'Pleased'), ('C', 'Neutral'), ('D', 'Needs Work'), ('F', 'Unacceptable')], max_length=1),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='quality_speed',
            field=models.CharField(choices=[('A', 'Very Pleased'), ('B', 'Pleased'), ('C', 'Neutral'), ('D', 'Needs Work'), ('F', 'Unacceptable')], max_length=1),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='quality_stability',
            field=models.CharField(choices=[('A', 'Very Pleased'), ('B', 'Pleased'), ('C', 'Neutral'), ('D', 'Needs Work'), ('F', 'Unacceptable')], max_length=1),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='quality_visual',
            field=models.CharField(choices=[('A', 'Very Pleased'), ('B', 'Pleased'), ('C', 'Neutral'), ('D', 'Needs Work'), ('F', 'Unacceptable')], max_length=1),
        ),
    ]