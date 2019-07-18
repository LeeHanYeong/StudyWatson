# Generated by Django 2.2.3 on 2019-07-18 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0004_auto_20190717_0224'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_withdraw', models.BooleanField(default=False, verbose_name='탈퇴여부')),
                ('role', models.CharField(choices=[('normal', '일반멤버'), ('sub_manager', '부 관리자'), ('manager', '관리자')], default='normal', max_length=12, verbose_name='역할')),
            ],
            options={
                'verbose_name': '스터디 멤버십',
                'verbose_name_plural': '스터디 멤버십 목록',
                'ordering': ('-pk',),
            },
        ),
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ('-pk',), 'verbose_name': '스터디 일정 참가', 'verbose_name_plural': '스터디 일정 참가 목록'},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ('-pk',), 'verbose_name': '스터디 일정', 'verbose_name_plural': '스터디 일정 목록'},
        ),
        migrations.AlterModelOptions(
            name='study',
            options={'ordering': ('-pk',), 'verbose_name': '스터디', 'verbose_name_plural': '스터디 목록'},
        ),
        migrations.AlterField(
            model_name='study',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_study_set', to=settings.AUTH_USER_MODEL, verbose_name='생성자'),
        ),
        migrations.DeleteModel(
            name='StudyMember',
        ),
        migrations.AddField(
            model_name='studymembership',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_set', to='study.Study', verbose_name='스터디'),
        ),
        migrations.AddField(
            model_name='studymembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_set', to=settings.AUTH_USER_MODEL, verbose_name='유저'),
        ),
        migrations.AddField(
            model_name='study',
            name='member_set',
            field=models.ManyToManyField(blank=True, related_name='joined_study_set', through='study.StudyMembership', to=settings.AUTH_USER_MODEL, verbose_name='스터디원 목록'),
        ),
    ]
