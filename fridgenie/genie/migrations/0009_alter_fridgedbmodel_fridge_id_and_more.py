# Generated by Django 4.2.2 on 2023-07-09 07:28

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0008_alter_fridgedbmodel_fridge_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgedbmodel',
            name='fridge_id',
            field=models.UUIDField(default=uuid.UUID('6f1647c2-3796-4969-8751-822a1c760cb7'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 9, 7, 28, 16, 260142, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 9, 7, 28, 16, 260157, tzinfo=datetime.timezone.utc)),
        ),
    ]
