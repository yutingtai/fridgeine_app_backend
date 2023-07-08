from django.db import models
from django.utils import timezone
import uuid


# Create your models here.

class FridgeDbModel(models.Model):
    fridge_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        unique=True)


class UserDbModel(models.Model):
    fridge_db_model = models.ForeignKey(FridgeDbModel, on_delete=models.CASCADE)


class CategoryDbModel(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class IngredientDbModel(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(CategoryDbModel, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=1)
    pic_url = models.CharField(max_length=100)
    fridge = models.ForeignKey(FridgeDbModel, on_delete=models.CASCADE)
    create_date = models.DateField(default=timezone.now())
    expiry_date = models.DateField(default=timezone.now())

    def __str__(self):
        return str(self.pk) + ". " + self.name
