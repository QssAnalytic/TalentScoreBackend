# Generated by Django 4.1.7 on 2023-09-12 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_alter_useraccountfilepage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportmodel',
            name='report_file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', to='users.useraccountfilepage'),
        ),
    ]