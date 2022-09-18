from django.shortcuts import render ,HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from videos.custom_auth.models import ApplicationUser
from videos.custom_auth.permissions import IsReadAction, IsSelf
from videos.post.models import Category, Post, Favourite
from videos.post.serializers import CategorySerializer, PostSerializer, FavouriteSerializer, UserDataSerializer, \
    UserPhotoSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering = 'name'
    filterset_fields = ('name',)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('created',)
    # ordering = 'created'
    filterset_fields = ('name', 'popular',)

    @action(methods=['get'], detail=False,  permission_classes=[permissions.IsAuthenticated, IsReadAction, IsSelf], url_path='user_data')
    def user_data(self, request, *args, **kwargs):
        print(self.request.user)
        serializer = UserDataSerializer(self.request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated, IsSelf], url_path='user_photo')
    def user_photo(self, request, *args, **kwargs):
        serializer = UserPhotoSerializer(data=self.request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self, *args, **kwargs):
    #     # queryset = super().get_queryset()
    #     queryset = Post.objects.filter(popular=True)
    #     print(queryset)
    #     data = {"data": queryset}
    #     return Response(queryset.count())


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('post',)
    filterset_fields = ('post',)


