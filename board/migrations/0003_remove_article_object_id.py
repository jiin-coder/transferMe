# Generated by Django 3.0.3 on 2022-01-12 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20220113_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='object_id',
        ),
    ]