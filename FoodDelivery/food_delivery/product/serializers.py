from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from food_delivery.custom_auth.serializers import BaseUserSerializer
from food_delivery.product.models import *


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('food', 'name',)
        read_only_fields = ('id',)


class FoodRatingSerializer(serializers.ModelSerializer):
    # total_comment = serializers.SerializerMethodField()

    class Meta:
        model = FoodRating
        fields = ('user', 'food', 'rating',)
        read_only_fields = ('id',)


class FoodSizeSerializer(serializers.ModelSerializer):
    # total_comment = serializers.SerializerMethodField()

    class Meta:
        model = FoodSize
        fields = list_display = ('food', 'size',)


class FoodSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()
    ingredient_food_details = IngredientSerializer(many=True, read_only=True)
    food_size_details = FoodSizeSerializer(read_only=True, many=True)
    # food_rating_details = FoodRatingSerializer(read_only=True, many=True)

    class Meta:
        model = Food
        fields = ('id', 'restaurant', 'food_name', 'slug', 'delivery_type', 'delivery_time', 'description', 'food_image', 'created', 'modified', 'ingredient_food_details', 'food_size_details', 'total_rating')
        read_only_fields = ('slug',)

    def get_total_rating(self, obj):
        total = FoodRating.objects.filter(food=obj).aggregate(total_rating=Avg("rating"))
        print("total", total)
        return total


class RestaurantRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantRating
        fields = ('user', 'restaurant', 'rating',)
        read_only_fields = ('id',)


class RestaurantSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    food_details = FoodSerializer(read_only=True, many=True)
    # ratings_details = RestaurantRatingSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'user', 'name', 'food_image', 'slug', 'created', 'modified', 'food_details', 'rating')
        read_only_fields = ('slug',)
        validators = [UniqueTogetherValidator(queryset=Restaurant.objects.all(), fields=('name',))]

    def get_rating(self, obj):
        total = RestaurantRating.objects.filter(restaurant=obj).aggregate(rating=Avg("rating"))
        return total


class FavoriteSerializer(serializers.ModelSerializer):
    food_details = FoodSerializer(read_only=True, required=False)
    user_details = BaseUserSerializer(required=False, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user_details', 'food_details', 'favorite_food')
        read_only_fields = ('id', 'user_details', 'food_details')
        extra_kwargs = {
            'favorite_food': {'required': True}
        }

    def create(self, validated_data):
        validated_data.update({'user_details': self.context['request'].user})
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    food_details = FoodSerializer(read_only=True, required=False)
    user_details = BaseUserSerializer(required=False, read_only=True)

    class Meta:
        model = Cart
        fields = ('user_details', 'food_details', 'quantity')
        read_only_fields = ('id', 'user_details', 'food_details')
        extra_kwargs = {
            'quantity': {'required': True}
        }

    def create(self, validated_data):
        validated_data.update({'user_details': self.context['request'].user})
        return super().create(validated_data)
