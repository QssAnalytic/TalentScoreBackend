# Generated by Django 4.1.7 on 2023-10-17 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, null=True)),
                ('native_language', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('report_test', models.BooleanField(blank=True, default=False, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to=users.models.user_profile_image_file_upath)),
            ],
            options={
                'verbose_name': 'UserAccount',
                'verbose_name_plural': 'UserAccounts',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserVerificationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.user_file_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserVerificationFile',
                'verbose_name_plural': 'UserVerificationFiles',
            },
        ),
        migrations.CreateModel(
            name='UserAccountFilePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_category', models.CharField(choices=[('CV', 'CV'), ('REPORT', 'REPORT'), ('CERTIFICATE', 'CERTIFICATE')], max_length=20)),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.user_account_file_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserAccountFilePage',
            },
        ),
        migrations.CreateModel(
            name='UniqueRandom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_value', models.CharField(max_length=32, unique=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UniqueRandom',
                'verbose_name_plural': 'UniqueRandoms',
            },
        ),
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_questions', models.JSONField(blank=True, null=True, verbose_name='Ümumi suallar')),
                ('secondary_education_questions', models.JSONField(blank=True, null=True, verbose_name='Orta, texniki və ali təhsil sualları')),
                ('olympiad_questions', models.JSONField(blank=True, null=True, verbose_name='Olimpiada sualları')),
                ('work_experience_questions', models.JSONField(blank=True, null=True, verbose_name='İş təcrübəsi')),
                ('special_skills_questions', models.JSONField(blank=True, null=True, verbose_name='Xüsusi bacarıqlar')),
                ('language_skills_questions', models.JSONField(blank=True, null=True, verbose_name='Dil bilikləri')),
                ('extra_language_skills_questions', models.JSONField(blank=True, null=True, verbose_name='Əlavə dil bilikləri')),
                ('special_skills_certificate_questions', models.JSONField(blank=True, null=True, verbose_name='Xüsusi bacarıq sertifikatları')),
                ('sport_questions', models.JSONField(blank=True, null=True, verbose_name='İdman sualları')),
                ('sport2_questions', models.JSONField(blank=True, null=True, verbose_name='İdman sualları2')),
                ('program_questions', models.JSONField(blank=True, null=True, verbose_name='Proqram bilikləri')),
                ('education_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('education_color', models.CharField(default='#00E5BC', max_length=30)),
                ('language_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('language_color', models.CharField(default='#FF0038', max_length=30)),
                ('special_skills_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('special_skills_color', models.CharField(default='#00A8E1', max_length=30)),
                ('sport_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('sport_color', models.CharField(default='#09959A', max_length=30)),
                ('work_experiance_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('work_experiance_color', models.CharField(default='#FFCB05', max_length=30)),
                ('program_score', models.DecimalField(decimal_places=13, default=1, max_digits=16)),
                ('program_color', models.CharField(default='#8800E0', max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('file_key', models.UUIDField(blank=True, null=True, unique=True)),
                ('report_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', to='users.useraccountfilepage')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ReportModel',
            },
        ),
        migrations.CreateModel(
            name='CertificateModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('file_key', models.UUIDField(blank=True, editable=False, null=True, unique=True)),
                ('certificate_file', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_file', to='users.useraccountfilepage')),
            ],
            options={
                'verbose_name': 'CertificateModel',
                'verbose_name_plural': 'CertificateModels',
            },
        ),
    ]
