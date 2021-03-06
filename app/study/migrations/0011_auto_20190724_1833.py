# Generated by Django 2.2.2 on 2019-07-24 09:33

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0010_auto_20190721_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyInviteToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('key', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='토큰값')),
                ('duration', models.PositiveSmallIntegerField(default=24, verbose_name='유효시간')),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.Study', verbose_name='스터디')),
            ],
            options={
                'verbose_name': '스터디 초대 토큰',
                'verbose_name_plural': '스터디 초대 토큰 목록',
                'ordering': ('-created',),
            },
        ),
        migrations.DeleteModel(
            name='StudyInviteLink',
        ),
        migrations.AddIndex(
            model_name='studyinvitetoken',
            index=models.Index(fields=['created'], name='study_study_created_3836ae_idx'),
        ),
        migrations.AddIndex(
            model_name='studyinvitetoken',
            index=models.Index(fields=['modified'], name='study_study_modifie_c807d8_idx'),
        ),
    ]
