from django.utils import timezone
import uuid

from django.conf import settings


def set_password_reset_expiration_time():
    return timezone.now() + timezone.timedelta(days=1)


def get_category_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.CATEGORY_PHOTO_PATH, uuid.uuid4(), filename)


def get_post_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.POST_PHOTO_PATH, uuid.uuid4(), filename)


def get_user_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.USER_PHOTO_PATH, uuid.uuid4(), filename)
