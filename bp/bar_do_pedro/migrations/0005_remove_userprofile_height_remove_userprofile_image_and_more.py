# Generated by Django 5.0.6 on 2024-09-05 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bar_do_pedro', '0004_remove_userprofile_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='weight',
        ),
    ]
