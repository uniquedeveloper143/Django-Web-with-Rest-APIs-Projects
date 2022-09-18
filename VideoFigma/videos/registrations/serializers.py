import phonenumbers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from phonenumber_field.serializerfields import PhoneNumberField
from videos.custom_auth.models import ApplicationUser


class CheckPhoneSerializer(Serializer):
    email = serializers.EmailField(required=True)


class CheckCodeSerializer(Serializer):
    OTP = serializers.CharField(required=True, max_length=4)


class CheckUserDataSerializer(ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ('email',  'password', )

        extra_kwargs = {
            'password': {'validators': [validate_password]},
            'email': {'required': True},
        }


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ('name', 'email', 'password', 'uuid',)
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
            'name': {'required': True},
        }
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assignment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user
