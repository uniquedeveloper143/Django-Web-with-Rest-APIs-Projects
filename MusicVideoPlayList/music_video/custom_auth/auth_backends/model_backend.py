from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.utils.translation import ugettext as _

from rest_framework.exceptions import PermissionDenied


class CustomModelBackend(ModelBackend):
    """
    Authenticate user using email or username
    """

    def authenticate(self, request, username=None, email=None, phone=None, password=None, **kwargs):
        if not username and not email and not phone:
            return None

        print("username", username)
        UserModel = get_user_model()

        if username:
            email = username

        if "@" not in username:
            phone = username

        # username_query_dict = {'username__iexact': username}
        email_query_dict = {'email__iexact': email}
        phone_query_dict = {'phone': phone}
        print("username", username)
        try:
            query_filter = Q()
            # if username:
            #     query_filter |= Q(**username_query_dict)
            if email:
                query_filter |= Q(**email_query_dict)
            if phone:
                query_filter |= Q(**phone_query_dict)

            user = UserModel.objects.get(query_filter)
            session = request.session['user'] = user.id
            print("user", user)
            print("session", session)
            if not user.is_active:
                raise PermissionDenied(_('User is not active.'))

        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None
