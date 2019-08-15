from rest_framework import serializers

from members.serializers import UserSerializer
from ..models import (
    StudyMembership,
    Attendance,
)
from .schedule import ScheduleSerializer
from .study import StudySerializer

STUDY_MEMBER_FIELDS = (
    'pk',
    'is_withdraw',
    'user',
    'study',
    'role',
    'role_display',

    'study_members',
    'study_schedules',
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
    study_members = UserSerializer(source='study.member_set', many=True)
    study_schedules = ScheduleSerializer(source='study.schedule_set', many=True)
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
