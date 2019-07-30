from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404

from members.serializers import UserSerializer
from utils.drf import errors
from utils.drf.exceptions import ValidationError
from .models import (
    StudyCategory,
    Study,
    StudyMembership,
    Attendance,
    Schedule,
    StudyInviteToken,
)

STUDY_FIELDS = (
    'pk',
    'category',
    'author',
    'name',
    'description',
)
STUDY_MEMBER_FIELDS = (
    'pk',
    'is_withdraw',
    'user',
    'study',
    'role',
    'role_display',
)
SCHEDULE_FIELDS = (
    'pk',
    'study',
    'location',
    'subject',
    'description',
    'vote_end_at',
    'start_at',
    'studying_time',

    'self_attendance',
)
ATTENDANCE_FIELDS = (
    'pk',
    'user',
    'schedule',
    'vote',
    'vote_display',
    'att',
    'att_display',
)


class StudyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCategory
        fields = (
            'pk',
            'name',
        )


class StudyMembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMembership
        fields = (
            'user',
            'study',
            'role',
        )

    def to_representation(self, instance):
        return StudyMembershipDetailSerializer(instance).data


class StudyMembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMembership
        fields = (
            'role',
        )

    def to_representation(self, instance):
        return StudyMembershipSerializer(instance).data


class ScheduleAttendanceSerializer(serializers.ModelSerializer):
    """
    Schedule detail에서 해당 Schedule에 속한 attendance_set을 나타내기 위한 Serializer
    """
    user = UserSerializer()
    vote_display = serializers.CharField(source='get_vote_display')
    att_display = serializers.CharField(source='get_att_display')

    class Meta:
        model = Attendance
        fields = (
            'pk',
            'user',
            'vote',
            'vote_display',
            'att',
            'att_display',
        )


class ScheduleSelfAttendanceSerializer(serializers.ModelSerializer):
    """
    Schedule list/detail에서 request.user가 존재할 경우,
    해당 User의 출석(Attendance)상태를 보여주기 위한 Serializer
    """
    vote_display = serializers.CharField(source='get_vote_display')
    att_display = serializers.CharField(source='get_att_display')

    class Meta:
        model = Attendance
        fields = (
            'pk',
            'vote',
            'vote_display',
            'att',
            'att_display',
        )


class ScheduleSerializer(serializers.ModelSerializer):
    self_attendance = ScheduleSelfAttendanceSerializer(
        help_text='인증된 사용자의 출석 객체, 인증되지 않았거나 없는경우 null', read_only=True,
    )

    class Meta:
        model = Schedule
        fields = SCHEDULE_FIELDS


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = SCHEDULE_FIELDS

    def to_representation(self, instance):
        return ScheduleSerializer(instance).data


class ScheduleDetailSerializer(ScheduleSerializer):
    attendance_set = ScheduleAttendanceSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = SCHEDULE_FIELDS + (
            'attendance_set',
        )


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = SCHEDULE_FIELDS

    def to_representation(self, instance):
        return ScheduleSerializer(instance).data


class StudySerializer(serializers.ModelSerializer):
    category = StudyCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Study
        fields = STUDY_FIELDS


class StudyMembershipAttendanceSerializer(serializers.ModelSerializer):
    vote_display = serializers.CharField(source='get_vote_display')
    att_display = serializers.CharField(source='get_att_display')
    schedule = ScheduleSerializer()

    class Meta:
        model = Attendance
        fields = (
            'pk',
            'schedule',
            'vote',
            'vote_display',
            'att',
            'att_display',
        )


class StudyMembershipSerializer(serializers.ModelSerializer):
    study = StudySerializer()
    user = UserSerializer()
    role_display = serializers.CharField(source='get_role_display')

    class Meta:
        model = StudyMembership
        fields = STUDY_MEMBER_FIELDS


class StudyMembershipDetailSerializer(StudyMembershipSerializer):
    attendance_set = StudyMembershipAttendanceSerializer(read_only=True, many=True)

    class Meta:
        model = StudyMembership
        fields = STUDY_MEMBER_FIELDS + (
            'attendance_set',
        )


class StudyDetailSerializer(StudySerializer):
    membership_set = StudyMembershipDetailSerializer(many=True)
    schedule_set = ScheduleDetailSerializer(many=True)

    class Meta:
        model = Study
        fields = STUDY_FIELDS + (
            'membership_set',
            'schedule_set',
        )


class StudyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = (
            'pk',
            'category',
            'name',
            'description',
        )

    def to_representation(self, instance):
        return StudySerializer(instance).data


class StudyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = (
            'category',
            'name',
            'description',
        )

    def to_representation(self, instance):
        return StudySerializer(instance).data


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    schedule = ScheduleSerializer()
    vote_display = serializers.CharField(source='get_vote_display')
    att_display = serializers.CharField(source='get_att_display')

    class Meta:
        model = Attendance
        fields = ATTENDANCE_FIELDS


class AttendanceDetailSerializer(AttendanceSerializer):
    study = StudySerializer(source='schedule__study')
    schedule = ScheduleSerializer()

    class Meta:
        model = Attendance
        fields = ATTENDANCE_FIELDS + (
            'study',
            'schedule',
        )


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'user',
            'schedule',
            'vote',
            'att',
        )

    def to_representation(self, instance):
        return AttendanceSerializer(instance).data


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'user',
            'vote',
            'att',
        )

    def to_representation(self, instance):
        return AttendanceSerializer(instance).data


class StudyInviteTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyInviteToken
        fields = (
            'key',
        )


class StudyInviteTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyInviteToken
        fields = (
            'study',
        )

    def to_representation(self, instance):
        return StudyInviteTokenSerializer(instance).data


class StudyMembershipCreateByInviteTokenSerializer(serializers.Serializer):
    key = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        key = validated_data.get('key')
        user = validated_data.get('user')
        if not (key and user):
            raise ValueError('key, user는 모두 존재해야 합니다')
        token = get_object_or_404(StudyInviteToken, key=key)

        membership, created = user.membership_set.get_or_create(study=token.study)
        if not created:
            if membership.is_withdraw:
                membership.is_withdraw = False
                membership.save()
            else:
                raise ValidationError(errors.MEMBERSHIP_ALREADY_EXISTS)
        return membership

    def update(self, instance, validated_data):
        raise MethodNotAllowed('update는 허용하지 않습니다')

    def to_representation(self, instance):
        return StudyMembershipSerializer(instance).data
