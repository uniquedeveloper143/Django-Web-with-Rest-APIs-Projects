from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from food_delivery.custom_auth.models import PasswordResetId
from food_delivery.custom_auth.serializers import AccessTokenSerializer, UserAuthSerializer, BaseUserSerializer
from food_delivery.registrations.serializers import PasswordSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'X-Token'
    access_token_serializer_class = AccessTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_access_token_serializer(self, **kwargs):
        return self.access_token_serializer_class(data=self.request.data, **kwargs)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(data=request.data, context={'request': request, 'view': self})
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        print(user)
        if not user:
            raise ValidationError("Invalid Users")

        user_details = BaseUserSerializer(
            instance=user, context={'request': request, 'view': self}).data
        user_details.update(self.get_success_headers(user)
                            )
        return Response(data=user_details, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_name='login', url_path='login')
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, **kwargs)  # for_agent=False,

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response("Logout Successfully", status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny], url_path='reset_password')
    def reset_password(self, request, *args, **kwargs):
        email1 = request.data.get('email')
        # phone_num = request.data.get('phone')

        # print('phone', phone_num)
        print('email', email1)

        if not email1:
            raise ValidationError("Email is required!")

        user_model = User

        email = user_model.objects.filter(email__iexact=email1).first()
        # phone = user_model.objects.filter(phone__iexact=phone_num).first()

        if not email:
            raise NotFound(_('User does not exists.'))
        else:
            password_id = PasswordResetId.objects.create(user=email)
        # if phone_num:
        #     phone = user_model.objects.filter(phone__iexact=phone_num).first()
        #     password_id = PasswordResetId.objects.create(user=phone)
        # if not email and not phone:
        #     raise NotFound(_('User does not exists.'))
        data = {"Reset_ID : ": password_id.id}
        return Response(data)

    @action(methods=['post'], detail=False, url_path='change_reset_password/(?P<reset_id>.*)',
            permission_classes=[permissions.AllowAny])
    def change_reset_password(self, request, *args, **kwargs):
        reset_id = get_object_or_404(PasswordResetId, pk=self.kwargs.get('reset_id'), expiration_time__gt=timezone.now())

        serializer = PasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=reset_id.user.id)
        user.set_password(serializer.data['password'])
        user.save()
        PasswordResetId.objects.filter(pk=reset_id.pk).delete()
        return Response(_('Password reset successfully!!'))
