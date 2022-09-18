from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from videos.post.models import Category, Post, Favourite, UserPhoto


class FavouriteInlines(admin.TabularInline):
    model = Favourite
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    list_display = ('id', 'user', 'name', 'post', 'slug')
    search_fields = ('slug', 'name', 'post')
    list_filter = ('name',)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    list_display = ('id', 'post_user', 'name', 'category', 'slug', 'description', 'popular', 'post')
    search_fields = ('name', 'popular', 'post')
    list_filter = ('name',  'category', 'popular',)
    inlines = (FavouriteInlines, )


class FavouriteAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    list_display = ('id', 'user', 'post', 'slug')
    search_fields = ('slug',)
    list_filter = ('slug',)


class UserPhotoAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('id', 'user', 'image', 'width', 'height')


admin.site.register(UserPhoto, UserPhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Favourite, FavouriteAdmin)
