# Generated by Django 5.0.6 on 2024-11-07 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bar_do_pedro', '0012_alter_drinksmade_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinks',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/'),
        ),
    ]