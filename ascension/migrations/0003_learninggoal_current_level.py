# Generated by Django 5.1.4 on 2025-01-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ascension', '0002_userinterest'),
    ]

    operations = [
        migrations.AddField(
            model_name='learninggoal',
            name='current_level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
