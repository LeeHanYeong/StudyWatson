# Generated by Django 2.2.3 on 2019-07-05 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='닉네임'),
        ),
    ]