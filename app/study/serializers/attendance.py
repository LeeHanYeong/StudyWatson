from rest_framework import serializers

from members.serializers import UserSerializer
from ..models import (
    Attendance,
)
from .schedule import ScheduleSerializer
from .study import StudySerializer

ATTENDANCE_FIELDS = (
    'pk',
    'user',
    'schedule',
    'vote',
    'vote_display',
    'att',
    'att_display',
)


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    schedule = ScheduleSerializer()
    vote_display = serializers.CharField(source='get_vote_display')
    att_display = serializers.CharField(source='get_att_display')

    class Meta:
        model = Attendance
        fields = ATTENDANCE_FIELDS


class AttendanceDetailSerializer(AttendanceSerializer):
    study = StudySerializer(source='schedule.study')
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
