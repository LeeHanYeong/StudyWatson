from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.crypto import get_random_string
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class StudyCategory(models.Model):
    name = models.CharField('카테고리명', max_length=20)

    class Meta:
        verbose_name = '스터디 카테고리'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class StudyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'category',
            'author',
        ).prefetch_related(
            'schedule_set',
            'schedule_set__attendance_set',
            'schedule_set__attendance_set__user',
            'membership_set',
            'membership_set__user',
        )

    def user_queryset(self, user):
        attendances = Attendance.objects.filter(user=user)
        return self.get_queryset().prefetch_related(
            Prefetch(
                'schedule_set__attendance_set',
                queryset=attendances,
                to_attr='self_attendance_list',
            )
        )


class Study(TimeStampedModel):
    category = models.ForeignKey(
        StudyCategory, verbose_name='카테고리',
        related_name='study_set', on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User, verbose_name='생성자', on_delete=models.CASCADE,
        related_name='created_study_set', blank=True, null=True,
    )
    name = models.CharField('스터디명', max_length=20)
    description = models.CharField('설명', max_length=100, blank=True)
    member_set = models.ManyToManyField(
        User, verbose_name='스터디원 목록', blank=True,
        through='StudyMembership', related_name='joined_study_set',
    )

    objects = StudyManager()

    class Meta:
        verbose_name = '스터디'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.category.name} | {self.name} (pk: {self.pk})'


class ScheduleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'study',
            'study__category',
        )

    def user_queryset(self, user):
        """
        request.user가 주어질 경우 필요한
            self_attendance (인증된 유저의 출석(Attendance) pk)
        를 annotate로 추가시켜주는 QuerySet
        :param user:
        :return:
        """
        self_attendances = Attendance.objects.filter(user=user)
        return self.get_queryset().prefetch_related(
            Prefetch(
                'attendance_set',
                queryset=self_attendances,
                to_attr='self_attendance_list',
            )
        )


class Schedule(TimeStampedModel):
    study = models.ForeignKey(
        Study, verbose_name='스터디', on_delete=models.CASCADE,
        related_name='schedule_set',
    )
    location = models.CharField('장소', max_length=50, blank=True)
    subject = models.CharField('주제', max_length=50, blank=True)
    description = models.CharField('설명', max_length=300, blank=True)
    vote_end_at = models.DateTimeField('투표 종료 일시', blank=True, null=True)
    start_at = models.DateTimeField('스터디 시작 일시', blank=True, null=True)
    studying_time = models.DurationField('스터디 시간', blank=True, null=True)

    objects = ScheduleManager()

    class Meta:
        verbose_name = '스터디 일정'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.study.category.name} | {self.study.name} | {self.start_at} (pk: {self.pk})'

    def save(self, **kwargs):
        super().save(**kwargs)
        # Schedule생성 시, Schedule의 생성보다 먼저 Study에 참여한 User들의 출석정보를 일괄 저장
        for memberhsip in self.study.membership_set.filter(
                created__lte=self.created):
            Attendance.objects.get_or_create(
                user=memberhsip.user,
                schedule=self,
            )

    @property
    def self_attendance(self):
        if hasattr(self, 'self_attendance_list'):
            try:
                return self.self_attendance_list[0]
            except IndexError:
                return None
        return None


class StudyMembership(TimeStampedModel):
    ROLE_NORMAL, ROLE_SUB_MANAGER, ROLE_MAIN_MANAGER = 'normal', 'sub_manager', 'manager'
    CHOICES_ROLE = (
        (ROLE_NORMAL, '일반멤버'),
        (ROLE_SUB_MANAGER, '부 관리자'),
        (ROLE_MAIN_MANAGER, '관리자'),
    )
    is_withdraw = models.BooleanField('탈퇴여부', default=False)
    user = models.ForeignKey(
        User, verbose_name='유저', on_delete=models.CASCADE,
        related_name='membership_set',
    )
    study = models.ForeignKey(
        Study, verbose_name='스터디', on_delete=models.CASCADE,
        related_name='membership_set',
    )
    role = models.CharField('역할', choices=CHOICES_ROLE, default=ROLE_NORMAL, max_length=12)

    class Meta:
        verbose_name = '스터디 멤버십'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)
        unique_together = (
            ('user', 'study'),
        )

    def __str__(self):
        return f'{self.study.name} | {self.user.name} ({self.get_role_display()} (pk: {self.pk})'

    def withdraw(self):
        self.is_withdraw = True
        self.save()

    @property
    def attendance_set(self):
        return self.user.attendance_set.filter(schedule__study=self.study)


class AttendanceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'user',
            'schedule',
        )


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
    vote = models.CharField('사전 참석 투표', choices=CHOICES_VOTE, max_length=10, blank=True)
    att = models.CharField('실제 참석 결과', choices=CHOICES_VOTE, max_length=10, blank=True)

    objects = AttendanceManager()

    class Meta:
        verbose_name = '스터디 일정 참가'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)
        unique_together = (
            ('user', 'schedule'),
        )

    def __str__(self):
        return f'{self.schedule.__str__()} | {self.user.name} ' \
            f'(사전: {self.get_vote_display()}, 실제: {self.get_att_display()}) ' \
            f'(pk: {self.pk})'


class StudyInviteToken(TimeStampedModel):
    study = models.ForeignKey(Study, verbose_name='스터디', on_delete=models.CASCADE)
    key = models.CharField('토큰값', max_length=30, blank=True, null=True, unique=True)
    duration = models.PositiveSmallIntegerField('유효시간', default=24)

    class Meta:
        verbose_name = '스터디 초대 토큰'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['modified']),
        ]

    def __str__(self):
        return f'{self.study.name}'

    def save(self, **kwargs):
        if not self.key:
            self.reset_code(commit=False)
        super().save(**kwargs)

    def is_valid(self):
        now = timezone.now()
        return now - self.created < timedelta(hours=self.duration)

    def reset_code(self, commit=True):
        while True:
            key = get_random_string(10)
            if not StudyInviteToken.objects.filter(key=key).exists():
                break

        self.key = key
        if commit:
            self.save()
