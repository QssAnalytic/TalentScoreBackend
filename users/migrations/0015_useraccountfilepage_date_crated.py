# Generated by Django 4.1.7 on 2023-08-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_uniquerandom_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccountfilepage',
            name='date_crated',
            field=models.DateField(blank=True, null=True),
        ),
    ]