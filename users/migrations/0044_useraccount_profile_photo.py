# Generated by Django 4.1.7 on 2023-10-12 06:59

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0043_alter_reportmodel_file_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_profile_image_file_upath),
        ),
    ]