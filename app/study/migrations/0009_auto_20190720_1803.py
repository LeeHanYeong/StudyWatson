# Generated by Django 2.2.3 on 2019-07-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_schedule_studying_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='studying_time',
            field=models.DurationField(blank=True, null=True, verbose_name='스터디 시간'),
        ),
    ]
