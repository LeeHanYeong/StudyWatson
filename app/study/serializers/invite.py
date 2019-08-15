from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import get_object_or_404

from utils.drf import errors
from utils.drf.exceptions import ValidationError
from ..models import (
    StudyInviteToken,
)


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
