# Generated by Django 5.1.4 on 2025-01-26 04:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_progress_unique_together'),
        ('ascension', '0007_category_interestcategory_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='learning_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ascension.learningplan'),
        ),
    ]
