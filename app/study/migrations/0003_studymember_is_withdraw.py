# Generated by Django 2.2.2 on 2019-07-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20190630_0447'),
    ]

    operations = [
        migrations.AddField(
            model_name='studymember',
            name='is_withdraw',
            field=models.BooleanField(default=False, verbose_name='탈퇴여부'),
        ),
    ]
