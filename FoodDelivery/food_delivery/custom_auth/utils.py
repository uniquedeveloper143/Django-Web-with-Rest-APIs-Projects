from django.utils import timezone
import uuid

from django.conf import settings


def set_password_reset_expiration_time():
    return timezone.now() + timezone.timedelta(days=1)


def get_restaurant_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.POST_RESTAURANT_PATH, uuid.uuid4(), filename)


def get_food_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.FOOD_PHOTO_PATH, uuid.uuid4(), filename)


def get_user_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.USER_PHOTO_PATH, uuid.uuid4(), filename)
