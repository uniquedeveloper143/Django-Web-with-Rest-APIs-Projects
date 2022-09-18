from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from music_video.post.models import Category, SubCategory, Post, Comment, CommentReply


class PostSerializer(serializers.ModelSerializer):
    total_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'sub_category', 'post_name', 'slug', 'description', 'post_image', 'post_media', 'total_comment')
        read_only_fields = ('slug',)

    def get_total_comment(self, obj):
        total = Comment.objects.filter(post=obj)
        return len(total)


class SubCategorySerializer(serializers.ModelSerializer):
    post_details = PostSerializer(read_only=True, many=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'sub_category_name', 'slug', 'post_details')
        read_only_fields = ('slug',)
        validators = [UniqueTogetherValidator(queryset=SubCategory.objects.all(), fields=('name',))]


class CategorySerializer(serializers.ModelSerializer):
    login_user = serializers.SerializerMethodField()
    category_details = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'slug', 'category_details', 'login_user')
        read_only_fields = ('slug',)
        validators = [UniqueTogetherValidator(queryset=Category.objects.all(), fields=('name',))]

    def get_login_user(self, obj):
        user = self.context['request'].user
        # print("user", user.username)
        # print("type", type(user))
        data = {'name': user.name, 'username': user.username}
        return data


class CommentSerializer(serializers.ModelSerializer):
    comment_post = PostSerializer(source='post', read_only=True)
    total_reply = serializers.SerializerMethodField()
    # comment_user = PostSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('comment_post', 'id', 'user', 'post', 'message', 'created',  'total_reply')
        read_only_fields = ('user', 'id', 'post')
        extra_kwargs = {
            'message': {'required': True}
        }

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        print(validated_data)
        return super().create(validated_data)

    def get_total_reply(self, obj):
        total = CommentReply.objects.filter(comment=obj)
        return len(total)


class CommentReplySerializer(serializers.ModelSerializer):

    comment_reply = CommentSerializer(source='comment', read_only=True)

    class Meta:
        model = CommentReply
        # print('time', 'created')
        fields = ('comment_reply', 'id', 'user', 'comment', 'message', 'created')
        read_only_fields = ('user', 'id', 'comment')
        extra_kwargs = {
            'message': {'required': True}
        }

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        return super().create(validated_data)


