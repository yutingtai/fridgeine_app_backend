from django.urls import path
from fridgenie.genie import views

urlpatterns = [
    path('fridge/<uuid:fridge_id>/', views.FridgeDetail.as_view(), name='Fridge_Detail'),
    path('fridge/<uuid:fridge_id>/ingredient/', views.Ingredient.as_view(), name='Create_Ingredient'),
    path('fridge/<uuid:fridge_id>/ingredient/<int:pk>', views.IngredientDetail.as_view(), name='Ingredient_Detail'),
    path('fridge/', views.NewFridge.as_view(), name='Create_Fridge'),
    path('fridge/<uuid:fridge_id>/recipe/', views.RecipeDetail.as_view(), name='Recipe_recommendation'),
]
