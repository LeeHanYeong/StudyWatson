from drf_extra_fields.fields import Base64ImageField
from rest_auth.serializers import TokenSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'img_profile',
            'username',
            'name',
            'nickname',
            'type',
            'email',
            'phone_number',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            ret['phone_number'] = instance.phone_number.as_national
        except AttributeError:
            pass
        return ret


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(help_text='비밀번호')
    password2 = serializers.CharField(help_text='비밀번호 확인')
    img_profile = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'img_profile',
            'username',
            'name',
            'nickname',
            'password1',
            'password2',
            'type',
            'email',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호와 비밀번호확인란의 값이 다릅니다')
        data['password'] = data['password2']
        del data['password1']
        del data['password2']
        return data

    def create(self, validated_data):
        return self.Meta.model._default_manager.create_user(**validated_data)

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=instance)[0]
        data = {
            'user': UserSerializer(instance).data,
            'token': token.key,
        }
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    img_profile = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'img_profile',
            'name',
            'nickname',
            'email',
            'phone_number',
        )

    def to_representation(self, instance):
        return UserSerializer(instance).data


class UserAttributeAvailableSerializer(serializers.Serializer):
    attribute_name = serializers.CharField()
    value = serializers.CharField()


class AuthTokenSerializer(TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + (
            'user',
        )
