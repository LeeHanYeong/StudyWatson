# Generated by Django 2.2.3 on 2019-07-21 08:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0009_auto_20190720_1803'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('user', 'schedule')},
        ),
        migrations.AlterUniqueTogether(
            name='studymembership',
            unique_together={('user', 'study')},
        ),
    ]