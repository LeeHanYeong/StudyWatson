from rest_framework import serializers

from members.serializers import UserSerializer
from ..models import (
    Attendance,
    Schedule,
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
