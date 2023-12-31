# Generated by Django 4.1.7 on 2023-08-28 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_certificatemodel_cert_file_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='certificatemodel',
            options={'verbose_name': 'CertificateModel', 'verbose_name_plural': 'CertificateModels'},
        ),
        migrations.AlterModelOptions(
            name='useraccountfilepage',
            options={'verbose_name': 'UserAccountFilePage'},
        ),
        migrations.RemoveField(
            model_name='reportmodel',
            name='file',
        ),
        migrations.AddField(
            model_name='certificatemodel',
            name='certificate_file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.useraccountfilepage'),
        ),
        migrations.AddField(
            model_name='reportmodel',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reportmodel',
            name='report_file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.useraccountfilepage'),
        ),
        migrations.AlterField(
            model_name='useraccountfilepage',
            name='file_category',
            field=models.CharField(choices=[('CV', 'CV'), ('REPORT', 'REPORT'), ('CERTIFICATE', 'CERTIFICATE')], max_length=20),
        ),
    ]
