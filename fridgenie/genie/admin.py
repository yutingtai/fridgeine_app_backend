from django.contrib import admin

# Register your models here.
from .models import IngredientDbModel, FridgeDbModel, UserDbModel, CategoryDbModel

admin.site.register(IngredientDbModel)
admin.site.register(FridgeDbModel)
admin.site.register(UserDbModel)
admin.site.register(CategoryDbModel)
