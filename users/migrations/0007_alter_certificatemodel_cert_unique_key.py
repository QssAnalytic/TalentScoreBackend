# Generated by Django 4.1.7 on 2023-08-24 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_certificatemodel_cert_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatemodel',
            name='cert_unique_key',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]
