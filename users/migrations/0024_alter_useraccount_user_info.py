# Generated by Django 4.1.7 on 2023-09-08 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_useraccount_user_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.reportmodel'),
        ),
    ]
