# Generated by Django 4.1.7 on 2023-09-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_answer_sub_answer_question_subanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='subanswer',
            name='sub_answer_weight',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='subanswer',
            name='sub_answer_weight_for_hashing',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
