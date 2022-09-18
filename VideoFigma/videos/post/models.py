from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from videos.custom_auth.utils import get_category_photo_path, get_post_photo_path, get_user_photo_path


class Category(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=150, unique=True,
                            error_messages={'unique': _('A category with that name already exists.')})
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    post = models.FileField(
        upload_to=get_category_photo_path,
        null=True,
        blank=True
      )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Post(TimeStampedModel):
    post_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(_('name'), max_length=250)
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    popular = models.BooleanField(null=True, blank=True, default=False)
    post = models.FileField(
        upload_to=get_post_photo_path,
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @staticmethod
    def get_products_by_id(all_id):
        return Post.objects.filter(id__in=all_id)

    @staticmethod
    def get_all_products():
        return Post.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Post.objects.filter(category=category_id)
        else:
            return Post.get_all_products()


class Favourite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _('Favourite')
        verbose_name_plural = _('Favourites')

    def __str__(self):
        return f'{self.post}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post)
        super().save(*args, **kwargs)


class UserPhoto(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_user_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('UserPhoto')
        verbose_name_plural = _('UserPhotos')

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = self.width
            self.height = self.height

        super().save(*args, **kwargs)
