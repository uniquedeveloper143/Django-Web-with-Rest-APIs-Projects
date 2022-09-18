from django.conf import settings
from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from music_video.custom_auth.utils import get_post_photo_path, get_post_media_path


class Category(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=150, unique=True,
                            error_messages={'unique': _('A category with that name already exists.')})
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)

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


class SubCategory(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_details")
    sub_category_name = models.CharField(_('SubCategory Name'), max_length=150, unique=True,
                            error_messages={'unique': _('A Subcategory with that name already exists.')})
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _('SubCategory')
        verbose_name_plural = _('SubCategories')

    def __str__(self):
        return f'{self.sub_category_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sub_category_name)
        super().save(*args, **kwargs)


class Post(TimeStampedModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='post_details')
    post_name = models.CharField(_('name'), max_length=250)
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    post_image = models.FileField(
        upload_to=get_post_photo_path,
        null=True,
        blank=True
    )
    post_media = models.FileField(
        upload_to=get_post_media_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f'{self.post_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_name)
        super().save(*args, **kwargs)


class Comment(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post")
    message = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.user}'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.post_name)
    #     super().save(*args, **kwargs)
    #


class CommentReply(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_reply")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_reply")
    message = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _('CommentReply')
        verbose_name_plural = _('CommentReplies')

    def __str__(self):
        return f'{self.user}'


class Like(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_like")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like", default=None)
    like_count = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f'{self.user}'


class DisLike(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_dislike")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_dislike")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_dislike", default=None)
    dislike_count = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = _('DisLike')
        verbose_name_plural = _('DisLikes')

    def __str__(self):
        return f'{self.user}'
