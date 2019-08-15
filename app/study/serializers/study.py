from rest_framework import serializers

from members.serializers import UserSerializer
from ..models import (
    StudyCategory,
    StudyIcon,
    Study,
    StudyMembership)

STUDY_FIELDS = (
    'pk',
    'category',
    'icon',
    'author',
    'name',
    'description',
)
STUDY_MEMBERSHIP_FIELDS = (
    'pk',
    'is_withdraw',
    'user',
    'study',
    'role',
    'role_display',
    'attendance_set',
)

__all__ = (
    'StudyCategorySerializer',
    'StudyCreateSerializer',
    'StudyIconSerializer',
    'StudySerializer',
    'StudyUpdateSerializer',
    'StudyDetailSerializer',
)


class StudyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCategory
        fields = (
            'pk',
            'name',
        )


class StudyIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyIcon
        fields = (
            'pk',
            'name',
            'image',
        )


class StudySerializer(serializers.ModelSerializer):
    category = StudyCategorySerializer()
    icon = StudyIconSerializer()
    author = UserSerializer()

    class Meta:
        model = Study
        fields = STUDY_FIELDS


class StudyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = (
            'pk',
            'category',
            'icon',
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
            'icon',
            'name',
            'description',
        )

    def to_representation(self, instance):
        return StudySerializer(instance).data


class _StudyDetailMembershipSerializer(serializers.ModelSerializer):
    """
    StudyDetailSerializer에서, membership_set을 표현하기 위한 Serializer
    """
    user = UserSerializer()
    role_display = serializers.CharField(source='get_role_display')

    class Meta:
        model = StudyMembership
        fields = STUDY_MEMBERSHIP_FIELDS


class StudyDetailSerializer(StudySerializer):
    from .schedule import ScheduleDetailSerializer

    membership_set = _StudyDetailMembershipSerializer(many=True)
    schedule_set = ScheduleDetailSerializer(many=True)

    class Meta:
        model = Study
        fields = STUDY_FIELDS + (
            'membership_set',
            'schedule_set',
        )
