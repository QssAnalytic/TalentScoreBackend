# Generated by Django 4.1.7 on 2023-08-25 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_merge_20230825_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userfile',
            name='user',
        ),
        migrations.DeleteModel(
            name='FileCategory',
        ),
        migrations.DeleteModel(
            name='UserFile',
        ),
    ]
