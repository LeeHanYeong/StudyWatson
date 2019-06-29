from rest_framework import serializers

from members.serializers import UserSerializer
from .models import (
    StudyCategory,
    Study,
    StudyMember,
    Attendance,
    Schedule,
)


class StudyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCategory
        fields = (
            'pk',
            'name',
        )


class StudyMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role_display = serializers.CharField(source='get_role_display')

    class Meta:
        model = StudyMember
        fields = (
            'pk',
            'user',
            'study',
            'role',
            'role_display',
        )


class StudyMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMember
        fields = (
            'user',
            'study',
            'role',
        )

    def to_representation(self, instance):
        return StudyMemberSerializer(instance).data


class StudyMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMember
        fields = (
            'role',
        )

    def to_representation(self, instance):
        return StudyMemberSerializer(instance).data


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'pk',
            'location',
            'description',
            'date',
            'due_date',
        )


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'study',
            'location',
            'description',
            'date',
            'due_date',
        )

    def to_representation(self, instance):
        return ScheduleSerializer(instance).data


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'location',
            'description',
            'date',
            'due_date',
        )

    def to_representation(self, instance):
        return ScheduleSerializer(instance).data


class StudySerializer(serializers.ModelSerializer):
    category = StudyCategorySerializer()
    author = UserSerializer()
    study_member_set = StudyMemberSerializer(many=True)
    schedule_set = ScheduleSerializer(many=True)

    class Meta:
        model = Study
        fields = (
            'pk',
            'category',
            'author',
            'name',
            'description',

            'study_member_set',
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
        fields = (
            'pk',
            'user',
            'schedule',
            'vote',
            'vote_display',
            'att',
            'att_display',
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
