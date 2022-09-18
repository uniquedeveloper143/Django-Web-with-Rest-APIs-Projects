from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from music_video.post.models import Category, SubCategory, Post, Comment, CommentReply, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('user', 'name', 'slug', 'created', 'modified')
    search_fields = ('user', 'name', 'slug')
    list_filter = ('user', 'name', 'slug')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('category', 'sub_category_name', 'slug', 'created', 'modified')
    search_fields = ('category', 'sub_category_name', 'slug')
    list_filter = ('category', 'sub_category_name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('sub_category', 'post_name', 'slug', 'description', 'post_image', 'post_media', 'created', 'modified')
    search_fields = ('sub_category', 'post_name', 'slug', )
    list_filter = ('sub_category', 'post_name', 'slug', )


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'message', 'created', 'modified')
    search_fields = ('user', 'post', 'message')
    list_filter = ('user', 'post', 'message')


@admin.register(CommentReply)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'message', 'created', 'modified')
    search_fields = ('user', 'comment', 'message')
    list_filter = ('user', 'comment', 'message')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'like_count', 'post', 'created', 'modified')
    search_fields = ('user', 'comment', 'like_count')
    list_filter = ('user', 'comment', 'like_count')

