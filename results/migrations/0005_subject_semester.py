# Generated by Django 4.2.6 on 2023-12-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_subject_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]