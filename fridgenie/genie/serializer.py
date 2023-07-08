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
        fields = ['name', 'category', 'amount', 'pic_url', 'create_date', 'expiry_date', 'fridge_id']


class UserDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDbModel
        fields = ['pk', 'fridge_db_model']


class FridgeDbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeDbModel
        fields = ['fridge_id']


class RecipeDetailSerializer(serializers.Serializer):
    ingredients = serializers.CharField(max_length=100)
