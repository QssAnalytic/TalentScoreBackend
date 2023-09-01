# Generated by Django 4.1.7 on 2023-08-25 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_userfile_category_remove_userfile_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserVerificationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.user_file_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]