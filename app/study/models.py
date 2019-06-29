from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class StudyCategory(models.Model):
    name = models.CharField('카테고리명', max_length=20)

    class Meta:
        verbose_name = '스터디 카테고리'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class Study(TimeStampedModel):
    category = models.ForeignKey(
        StudyCategory, verbose_name='카테고리',
        related_name='study_set', on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User, verbose_name='작성자', on_delete=models.CASCADE,
        related_name='study_set', blank=True, null=True,
    )
    name = models.CharField('스터디명', max_length=20)
    description = models.CharField('설명', max_length=100, blank=True)

    class Meta:
        verbose_name = '스터디'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.category.name} | {self.name}'


class Schedule(TimeStampedModel):
    study = models.ForeignKey(
        Study, verbose_name='스터디', on_delete=models.CASCADE,
        related_name='schedule_set',
    )
    location = models.CharField('장소', max_length=50, blank=True)
    description = models.CharField('설명', max_length=300, blank=True)
    date = models.DateField('일정 당일')
    due_date = models.DateField('마감일', blank=True, null=True)

    class Meta:
        verbose_name = '스터디 일정'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.study.category.name} | {self.study.name} | {self.date}'


class StudyMember(TimeStampedModel):
    ROLE_NORMAL, ROLE_SUB_MANAGER, ROLE_MAIN_MANAGER = 'normal', 'sub_manager', 'manager'
    CHOICES_ROLE = (
        (ROLE_NORMAL, '일반멤버'),
        (ROLE_SUB_MANAGER, '부 관리자'),
        (ROLE_MAIN_MANAGER, '관리자'),
    )
    user = models.ForeignKey(
        User, verbose_name='유저', on_delete=models.CASCADE,
        related_name='study_member_set',
    )
    study = models.ForeignKey(
        Study, verbose_name='스터디', on_delete=models.CASCADE,
        related_name='study_member_set',
    )
    role = models.CharField('역할', choices=CHOICES_ROLE, default=ROLE_NORMAL, max_length=12)

    class Meta:
        verbose_name = '스터디 멤버'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.study.name} | {self.user.name} ({self.get_role_display()}'


class Attendance(TimeStampedModel):
    VOTE_ATTEND, VOTE_LATE, VOTE_ABSENT = ('attend', 'late', 'absent')
    CHOICES_VOTE = (
        (VOTE_ATTEND, '참석'),
        (VOTE_LATE, '지각'),
        (VOTE_ABSENT, '결석'),
    )
    user = models.ForeignKey(
        User, verbose_name='유저', on_delete=models.CASCADE,
        related_name='attendance_set',
    )
    schedule = models.ForeignKey(
        Schedule, verbose_name='스터디 일정', on_delete=models.CASCADE,
        related_name='attendance_set',
    )
    vote = models.CharField('사전 참석 투표', choices=CHOICES_VOTE, max_length=10)
    att = models.CharField('실제 참석 결과', choices=CHOICES_VOTE, max_length=10, blank=True)

    class Meta:
        verbose_name = '스터디 일정 참가'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.schedule.__str__()} | {self.user.name} (사전: {self.get_vote_display()}, 실제: {self.get_att_display()()}'
