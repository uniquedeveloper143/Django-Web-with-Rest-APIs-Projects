from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from music_video.custom_auth.permissions import IsReadAction, IsSelf
from music_video.post.models import Category, Post, SubCategory, Comment, CommentReply
from music_video.post.serializers import CategorySerializer, SubCategorySerializer, PostSerializer, CommentSerializer, CommentReplySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering = 'name'
    filterset_fields = ('name',)


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('sub_category_name',)
    ordering = 'sub_category_name'
    filterset_fields = ('sub_category_name',)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]

    # lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('post_name',)
    ordering = 'post_name'
    ordering_fields = ('post_name',)
    filterset_fields = ('post_name',)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='add_post_comment')
    def add_post_comment(self, request, *args, **kwargs):
        post_data = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data.update({"post": post_data})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path="post_comment_reply")
    def post_comment_reply(self, request, *args, **kwargs):
        comment_data = self.get_object()
        serializer = CommentReplySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.update({"comment": comment_data})
        serializer.save()
        return Response(serializer.data)

    # @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated], url_path='add_comment')
    # def add_comment(self, request, *args, **kwargs):
    #     serializer = CommentSerializer(data=self.request.data, context={'request': request})
    #     # print(serializer)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]


    # @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated], url_path='reply_comment')
    # def reply_comment(self, request, *args, **kwargs):
    #     # comment = self.get_object()
    #     serializer = CommentReplySerializer(data=self.request.data, context={'request': request})
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


