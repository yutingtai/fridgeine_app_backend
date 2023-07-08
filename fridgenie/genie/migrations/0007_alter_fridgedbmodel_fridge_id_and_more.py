# Generated by Django 4.2.2 on 2023-06-21 09:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0006_alter_fridgedbmodel_fridge_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgedbmodel',
            name='fridge_id',
            field=models.UUIDField(default=uuid.UUID('7f917685-ab86-4e0d-bfe4-448a02a680f2'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 21, 9, 22, 49, 575132, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 21, 9, 22, 49, 575132, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userdbmodel',
            name='fridge_db_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genie.fridgedbmodel'),
        ),
    ]