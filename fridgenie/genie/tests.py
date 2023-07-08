from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import IngredientDbModel, UserDbModel, FridgeDbModel
from .serializer import IngredientDbModelSerializer


# TestCase already set up the APIClint(), I don't need to to that
class NewFridgeCreateAndGetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_get_fridge(self):
        url = reverse('Create_Fridge')
        response_post = self.client.post(url, format='json')

        fridge = FridgeDbModel.objects.get()
        url = reverse('Fridge_Detail', kwargs={'fridge_id': fridge.fridge_id})
        response_get = self.client.get(url, format='json')

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(FridgeDbModel.objects.count(), 1)
        self.assertEqual(UserDbModel.objects.count(), 1)


class IngredientCreateAndGetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fridge = FridgeDbModel()
        self.fridge.save()

    def test_create_and_get_ingredient(self):
        fridge = self.fridge
        fridge_id = fridge.fridge_id
        url = reverse('Create_Ingredient', kwargs={'fridge_id': fridge_id})
        data = {
            "name": "string",
            "amount": 0,
            "pic_url": "string",
            "create_date": "2023-06-21",
            "expiry_date": "2023-06-21"
        }

        response_post = self.client.post(url, data, format='json')

        ingredient = IngredientDbModel.objects.get()
        url_get = reverse('Ingredient_Detail',
                          kwargs={'fridge_id': fridge_id, 'pk': ingredient.pk})
        response_get = self.client.get(url_get)
        serializer = IngredientDbModelSerializer(ingredient)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(IngredientDbModel.objects.count(), 1)
        self.assertEqual(response_post.data, serializer.data)


class IngredientCreateAndModifyAndDeleteTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fridge = FridgeDbModel()
        self.fridge.save()

    def test_create_and_modify_ingredient(self):
        fridge = self.fridge
        fridge_id = fridge.fridge_id
        url = reverse('Create_Ingredient', kwargs={'fridge_id': fridge_id})
        data = {
            "name": "string",
            "amount": 0,
            "pic_url": "string",
            "create_date": "2023-06-21",
            "expiry_date": "2023-06-21"
        }
        response_create = self.client.post(url, data, format='json')
        ingredient = IngredientDbModel.objects.get()
        ingredient_id = ingredient.pk
        url_modify = reverse('Ingredient_Detail',
                             kwargs={'fridge_id': fridge_id, 'pk': ingredient_id})
        data_modify = {
            "name": "tomato",
            "amount": 2,
            "pic_url": "string",
            "create_date": "2023-06-21",
            "expiry_date": "2023-06-30",
            "fridge_id": f"{fridge_id}"
        }
        response = self.client.put(url_modify, data_modify, format='json')
        modified_ingredient = IngredientDbModel.objects.get(name='tomato')

        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(IngredientDbModel.objects.count(), 1)
        self.assertEqual(modified_ingredient.name, 'tomato')
        self.assertEqual(modified_ingredient.amount, 2)

    def test_create_and_delete_ingredient(self):
        fridge = self.fridge
        fridge_id = fridge.fridge_id
        url = reverse('Create_Ingredient', kwargs={'fridge_id': fridge_id})
        data = {
            "name": "tomato",
            "amount": 3,
            "pic_url": "string",
            "create_date": "2023-06-21",
            "expiry_date": "2023-06-28"
        }
        response_create = self.client.post(url, data, format='json')
        ingredient_id = IngredientDbModel.objects.get().pk
        url_delete = reverse('Ingredient_Detail',
                             kwargs={'fridge_id': fridge_id, 'pk': ingredient_id})
        response = self.client.delete(url_delete)
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IngredientDbModel.objects.count(), 0)


class FailIngredientCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fridge = FridgeDbModel()
        self.fridge.save()

    def test_create_new_ingredient(self):
        fridge_id = self.fridge.fridge_id
        url = reverse('Create_Ingredient', kwargs={'fridge_id': fridge_id})
        data = {
            "name": "tomato",
            "category": "wrong_category",
            "amount": 2,
            "pic_url": "string",
            "create_date": "2023-06-21",
            "expiry_date": "2023-06-21"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetRecipeRecommendation(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fridge = FridgeDbModel()
        self.fridge.save()

    def test_get_the_recipe(self):
        fridge_id = self.fridge.fridge_id
        url = reverse('Recipe_recommendation', kwargs={'fridge_id': fridge_id})
        data = {
            "ingredients": "['pineapple', 'green onion', 'pepper, spinach']"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
