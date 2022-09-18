from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from food_delivery.custom_auth.permissions import IsReadAction, IsSelf
from food_delivery.product.models import *
from food_delivery.product.serializers import *


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction, IsSelf]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering = 'name'
    filterset_fields = ('name',)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('food_name',)
    ordering = 'food_name'
    filterset_fields = ('food_name',)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='add_cart')
    def add_cart(self, request, *args, **kwargs):
        food_data = self.get_object()
        serializer = CartSerializer(data=request.data, context={'request': request})
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data.update({"food_details": food_data})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated], url_path='add_favorite')
    def add_favorite(self, request, *args, **kwargs):
        food_data = self.get_object()
        serializer = FavoriteSerializer(data=request.data, context={'request': request})
        print(serializer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data.update({"food_details": food_data})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FoodSizeViewSet(viewsets.ModelViewSet):
    queryset = FoodSize.objects.all()
    serializer_class = FoodSizeSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]


class FoodRatingViewSet(viewsets.ModelViewSet):
    queryset = FoodRating.objects.all()
    serializer_class = FoodRatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]


class RestaurantRatingViewSet(viewsets.ModelViewSet):
    queryset = RestaurantRating.objects.all()
    serializer_class = RestaurantRatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('food_details',)
    ordering = 'food_details'
    filterset_fields = ('food_details',)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelf]

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('favorite_food',)
    ordering = 'favorite_food'
    filterset_fields = ('favorite_food',)

