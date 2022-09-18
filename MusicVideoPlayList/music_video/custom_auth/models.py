import uuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from music_video.custom_auth.managers import ApplicationUserManager
from music_video.custom_auth.utils import set_password_reset_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    PermissionsMixin,
):
    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that uuid already exists.'),
        },
        default=uuid.uuid4,
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True,
                              error_messages={
                                  'unique': _('A user with that email already exists.'),
                              },
                              )
    is_email_verified = models.BooleanField('email verified', default=True)
    name = models.CharField(_('Name'), max_length=150, blank=True,
                            help_text=_('Name as it was returned by social provider'))

    is_active = models.BooleanField(_('staff status'), default=True, help_text=_(
        'Designates whether the user can log into this admin site.'
    ),
                                    )
    is_staff = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect theis instead of deleting accounts.'),
                                   )

    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    phone = PhoneNumberField(_('phone'), null=True, unique=True, blank=True,
                             error_messages={
                                 'unique': _('A user with that phone already exists.'),
                             },
                             )

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username or self.name or self.email or str(self.uuid)

    def update_last_activity(self):
        now = timezone.now()

        self.last_user_activity = now
        self.save(update_fields=('last_user_activity', 'last_modified'))


class PasswordResetId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=set_password_reset_expiration_time)

    class Meta:
        verbose_name = 'Password reset id'
