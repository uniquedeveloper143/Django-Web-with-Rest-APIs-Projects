from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from videos.custom_auth.models import ApplicationUser
from videos.post.models import Category, Post, Favourite, UserPhoto


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'user', 'post', 'slug')

        read_only_fields = ('slug', )

        validators = [UniqueTogetherValidator(queryset=Category.objects.all(), fields=('name',))]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_user', 'category', 'name', 'popular', 'post', 'description', 'slug')

        read_only_fields = ('slug', )

        # validators = [UniqueTogetherValidator(queryset=Post.objects.all(), fields=('name',))]


class FavouriteSerializer(serializers.ModelSerializer):
    # user_details = CategorySerializer(source='user', read_only=True)
    post_details = PostSerializer(source='post', read_only=True)

    class Meta:
        model = Favourite
        fields = ('id',  'post_details', 'slug')
        # fields = "__all__"

        read_only_fields = ('slug', )


class UserPhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = UserPhoto
        fields = ('id', 'image', 'width', 'height')

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        return super().create(validated_data)


class UserDataSerializer(serializers.ModelSerializer):
    user_photo = UserPhotoSerializer(read_only=True, many=True)

    class Meta:
        model = ApplicationUser
        fields = ('name', 'username', 'uuid', 'email', 'user_photo')
