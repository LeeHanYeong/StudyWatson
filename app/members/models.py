import string

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import DeleteModel, DeleteModelManager


class UserManager(DeleteModelManager, BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if extra_fields.get('type') == User.TYPE_EMAIL:
            username = email
        elif username is None:
            raise ValidationError('사용자 생성 필수값(username)이 주어지지 않았습니다')
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel, DeleteModel):
    TYPE_KAKAO, TYPE_FACEBOOK, TYPE_GOOGLE, TYPE_EMAIL = 'kakao', 'facebook', 'google', 'email'
    TYPE_CHOICES = (
        (TYPE_KAKAO, '카카오'),
        (TYPE_FACEBOOK, '페이스북'),
        (TYPE_GOOGLE, '구글'),
        (TYPE_EMAIL, '이메일'),
    )
    first_name = None
    last_name = None
    img_profile = models.ImageField('프로필 이미지', upload_to='user', blank=True)
    name = models.CharField('이름', max_length=20, blank=True)
    nickname = models.CharField('닉네임', max_length=20, blank=True, null=True)
    type = models.CharField('유형', max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL)
    email = models.EmailField('이메일', unique=True, null=True)
    phone_number = PhoneNumberField('전화번호', blank=True)

    # Deleted
    deleted_email = models.EmailField('삭제된 유저의 이메일', blank=True)
    deleted_username = models.CharField('삭제된 유저의 username', max_length=150, blank=True)
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    def __str__(self):
        return f'{self.name} ({self.email}) (pk: {self.pk})'

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        if self.type == self.TYPE_EMAIL and not self.is_deleted:
            self.username = self.email
        super().save(*args, **kwargs)

    def perform_delete(self):
        self.deleted_username = self.username
        self.deleted_email = self.email
        last_deleted_user = User._base_manager.filter(is_deleted=True).order_by('username').last()
        if last_deleted_user:
            number = int(last_deleted_user.username.rsplit('_', 1)[-1])
        else:
            number = 0
        deleted_name = f'deleted_{number:05d}'
        self.username = deleted_name
        self.email = None


class EmailValidation(TimeStampedModel):
    user = models.OneToOneField(
        User, verbose_name='사용자', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField('이메일')
    code = models.CharField('인증코드', max_length=50)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(6, allowed_chars=string.digits)
        super().save(*args, **kwargs)
