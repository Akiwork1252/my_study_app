# Generated by Django 5.1.4 on 2025-01-20 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_progress_completed_at_progress_started_at_and_more'),
        ('ascension', '0007_category_interestcategory_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='learning_goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ascension.learninggoal'),
        ),
    ]
