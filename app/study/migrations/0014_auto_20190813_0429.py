# Generated by Django 2.2.4 on 2019-08-12 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0013_auto_20190810_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyicon',
            name='image',
            field=models.ImageField(blank=True, upload_to='study/icons/', verbose_name='아이콘 이미지'),
        ),
    ]
