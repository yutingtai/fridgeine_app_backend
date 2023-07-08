from abc import ABC

from rest_framework import serializers
from .models import UserDbModel, IngredientDbModel, FridgeDbModel, CategoryDbModel


class CategoryDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDbModel
        fields = ['name']


class IngredientDbModelSerializer(serializers.ModelSerializer):
    fridge_id = serializers.UUIDField()

    class Meta:
        model = IngredientDbModel
        fields = ['name', 'category', 'amount', 'pic_url', 'create_date', 'expiry_date', 'fridge_id', 'pk']


class UserDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDbModel
        fields = ['pk', 'fridge_db_model']


class FridgeDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeDbModel
        fields = ['fridge_id']


class RecipeDetailSerializer(serializers.Serializer):
    a_lot_of_recipe = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=200)
    ingredients = serializers.CharField(max_length=500)


class RecipeRecommendationRequireDate(serializers.Serializer):
    ingredients = serializers.CharField()