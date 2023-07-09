from dotenv import load_dotenv, find_dotenv

from .models import FridgeDbModel, IngredientDbModel, UserDbModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .serializer import IngredientDbModelSerializer, UserDbModelSerializer, RecipeDetailSerializer, \
    RecipeRecommendationRequireDate
import requests
import json
import re
import os

from typing import List
from drf_spectacular.utils import extend_schema


class FridgeDetail(APIView):
    """
    Get and create the ingredients in the fridge.
    """

    def get_serializer_class(self):
        return IngredientDbModelSerializer

    @extend_schema(responses=IngredientDbModelSerializer(many=True))
    def get(self, request, fridge_id, format=None):
        fridge_model: FridgeDbModel = FridgeDbModel.objects.get(pk=fridge_id)
        ingredients = fridge_model.ingredientdbmodel_set.all()
        serializer = IngredientDbModelSerializer(ingredients, many=True)
        return Response(serializer.data)


class Ingredient(APIView):
    def get_serializer_class(self):
        return IngredientDbModelSerializer

    @extend_schema(responses=IngredientDbModelSerializer)
    def post(self, request, fridge_id, format=None):
        request.data['fridge_id'] = fridge_id
        serializer = IngredientDbModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetail(APIView):
    def get_serializer_class(self):
        return IngredientDbModelSerializer

    def get_object(self, pk):
        try:
            return IngredientDbModel.objects.get(pk=pk)
        except IngredientDbModel.DoesNotExist:
            raise Http404

    @extend_schema(responses=IngredientDbModelSerializer)
    def get(self, request, fridge_id, pk, format=None):
        ingredient = self.get_object(pk)
        serializer = IngredientDbModelSerializer(ingredient)
        return Response(serializer.data)

    @extend_schema(responses=IngredientDbModelSerializer)
    def put(self, request, fridge_id, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientDbModelSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fridge_id, pk, format=None):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewFridge(APIView):
    # def get_serializer_class(self):
    #     return UserDbModelSerializer

    @extend_schema(responses=UserDbModelSerializer)
    def post(self, request, format=None):
        new_fridge = FridgeDbModel()
        new_fridge.save()
        new_user = UserDbModel(fridge_db_model=new_fridge)
        new_user.save()
        serializer = UserDbModelSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecipeDetail(APIView):
    def get_serializer_class(self):
        return RecipeDetailSerializer

    @extend_schema(request=RecipeRecommendationRequireDate, responses=RecipeDetailSerializer(many=True))
    def post(self, request, fridge_id):
        some_names_of_recipe = self.get_the_name_of_recipe(request.data["ingredients"])
        a_lot_of_recipe = self.get_the_recipe_from_the_name(some_names_of_recipe)
        return a_lot_of_recipe

    def get_the_name_of_recipe(self, ingredients):
        headers = {"Content-Type": "application/json"}
        content = "Recommend me some dishes that I might be able to cook base on what ingredients I have in the fridge. The format follows the example below: I have banana, eggs, spinach, spaghetti. Your reply:Banana pancake, Spinach and Egg Scramble, Spinach and Banana Smoothie, Spaghetti with Spinach and Eggs.Please only reply the name of dishes without cooking instruction in one line that separated by comma. I have " + ingredients
        data = json.dumps({
            "model": "text-davinci-003",
            "prompt": f"{content}",
            "max_tokens": 60,
            "temperature": 0
        })

        CHATGPT_API_URL = os.environ['CHATGPT_API_URL']
        r = requests.post(CHATGPT_API_URL, data=data, headers=headers).json()
        recipe_name = r['choices'][0]['text']
        some_names_of_recipe = [content for content in re.split('\.|\,|\n', recipe_name) if content != '']
        return some_names_of_recipe

    def get_the_recipe_from_the_name(self, some_names_of_recipe: List):
        app_id = 'a8b39f46'
        RECIPE_API_KEY = os.environ['RECIPE_API_KEY']
        a_lot_of_recipe = []
        for name in some_names_of_recipe:
            number_of_recipe = 0
            r = requests.get(
                f'https://api.edamam.com/api/recipes/v2?type=public&q={name}&app_id={app_id}&app_key={RECIPE_API_KEY}&random=true')
            for stuff in r.json()['hits'][0:20]:
                recipe = {}
                website_exists = False
                try:
                    if requests.get(stuff['recipe']['url']).status_code == 200:
                        website_exists = True
                except requests.exceptions.ConnectTimeout:
                    website_exists = False
                if stuff['recipe']['image'] and website_exists:
                    recipe['name'] = stuff['recipe']['label']
                    recipe['image'] = stuff['recipe']['image']
                    recipe['url'] = stuff['recipe']['url']
                    recipe['ingredients'] = stuff['recipe']['ingredientLines']
                    a_lot_of_recipe.append(recipe)
                    number_of_recipe += 1
                    if number_of_recipe == 2:
                        break
            if len(a_lot_of_recipe) == 6:
                break
        return Response(a_lot_of_recipe, status=status.HTTP_200_OK)
