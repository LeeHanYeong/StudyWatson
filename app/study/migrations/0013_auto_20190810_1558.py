# Generated by Django 2.2.2 on 2019-08-10 06:58
import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import migrations


def forwards_func(apps, schema_editor):
    StudyIcon = apps.get_model('study', 'StudyIcon')
    db_alias = schema_editor.connection.alias

    icon_image_dir = os.path.join(settings.STATIC_DIR, 'init', 'study', 'StudyIcon', 'icon_image')

    StudyIcon.objects.using(db_alias).bulk_create([
        StudyIcon(
            name=filename.rsplit('.', 1)[0],
            image=SimpleUploadedFile(
                name=filename,
                content=open(os.path.join(icon_image_dir, filename), 'rb').read(),
            ),
        ) for filename in os.listdir(icon_image_dir)
    ])


def reverse_func(apps, schema_editor):
    StudyIcon = apps.get_model('study', 'StudyIcon')
    db_alias = schema_editor.connection.alias
    StudyIcon.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('study', '0012_auto_20190810_1558'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]