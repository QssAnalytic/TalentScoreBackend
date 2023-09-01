# Generated by Django 4.1.7 on 2023-08-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_uniquerandom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatemodel',
            name='cert_image',
        ),
        migrations.AddField(
            model_name='certificatemodel',
            name='cert_unique_key',
            field=models.CharField(default='ab4ef8b41fb1400d97ec6934ab9df3da', max_length=32, unique=True),
        ),
    ]