# Generated by Django 4.1.7 on 2023-10-09 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_county'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='County',
            new_name='Country',
        ),
    ]