import phonenumbers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_framework.serializers import ModelSerializer, Serializer

from phonenumber_field.serializerfields import PhoneNumberField

from food_delivery.custom_auth.models import ApplicationUser


class CheckPhoneSerializer(Serializer):
    phone = PhoneNumberField(required=True)


class CheckCodeSerializer(Serializer):
    OTP = serializers.CharField(required=True, max_length=4)


class CheckUserDataSerializer(ModelSerializer):
    # phone = PhoneNumberField()
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationUser
        fields = ('email', 'phone', 'password', 'country_code', 'phone_number')

        extra_kwargs = {
            'password': {'validators': [validate_password]},
            'email': {'required': True},
            'phone': {'required': True},
        }

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj['phone']))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj['phone']))
            return str(phone.national_number)
        except phonenumbers.NumberParseException:
            return None


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ('name', 'email', 'phone', 'password', 'uuid', )
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
            'name': {'required': True},
            'phone': {'required': True},
        }
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assignment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
