from rest_framework import serializers

from members.serializers import UserSerializer
from .models import (
    StudyCategory,
    Study,
    StudyMembership,
    Attendance,
    Schedule,
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


class StudyMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMembership
        fields = (
            'user',
            'study',
            'role',
        )

    def to_representation(self, instance):
        return StudyMembershipDetailSerializer(instance).data


class StudyMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMembership
        fields = (
            'role',
        )

    def to_representation(self, instance):
        return StudyMembershipSerializer(instance).data


class ScheduleSerializer(serializers.ModelSerializer):
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
    class Meta:
        fields = SCHEDULE_FIELDS


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


class StudyMembershipSerializer(serializers.ModelSerializer):
    study = StudySerializer()
    user = UserSerializer()
    role_display = serializers.CharField(source='get_role_display')

    class Meta:
        model = StudyMembership
        fields = STUDY_MEMBER_FIELDS


class AttendanceSimpleSerializer(serializers.ModelSerializer):
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


class StudyMembershipDetailSerializer(StudyMembershipSerializer):
    attendance_set = AttendanceSimpleSerializer(read_only=True, many=True)

    class Meta:
        model = StudyMembership
        fields = STUDY_MEMBER_FIELDS + (
            'attendance_set',
        )


class StudyDetailSerializer(StudySerializer):
    membership_set = StudyMembershipDetailSerializer(many=True)
    schedule_set = ScheduleSerializer(many=True)

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
