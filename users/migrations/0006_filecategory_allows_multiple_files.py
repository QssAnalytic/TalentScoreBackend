# Generated by Django 4.1.7 on 2023-08-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_filecategory_userfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecategory',
            name='allows_multiple_files',
            field=models.BooleanField(default=False),
        ),
    ]
