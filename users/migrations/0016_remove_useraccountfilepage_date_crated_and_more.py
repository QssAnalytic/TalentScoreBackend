# Generated by Django 4.1.7 on 2023-08-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_useraccountfilepage_date_crated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccountfilepage',
            name='date_crated',
        ),
        migrations.RemoveField(
            model_name='useraccountfilepage',
            name='file_key',
        ),
        migrations.AddField(
            model_name='certificatemodel',
            name='file_key',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='reportmodel',
            name='file_key',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]