import phonenumbers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
User = get_user_model()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1020)


class UserAuthSerializer(serializers.Serializer):
    # username = serializers.CharField(required=False)   # Username login is not allowed
    # name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if 'email' not in validated_data and 'phone' not in validated_data:
            raise ValidationError(_('Email or Phone should be provided'))
        return validated_data


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'uuid', 'name',  'email', 'phone', 'password', 'country_code', 'phone_number')
        read_only_fields = ('uuid',)

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def create(self, validated_data):
        user = self.get_user()
        validated_data['user'] = user

        return super().create(validated_data)

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return str(phone.national_number)
        except phonenumbers.NumberParseException:
            return None

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        user = super().save(**kwargs)
        # password assignment
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user
