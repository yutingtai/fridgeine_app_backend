# Generated by Django 4.2.2 on 2023-06-21 07:48

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0004_remove_categorydbmodel_id_alter_categorydbmodel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgedbmodel',
            name='fridge_id',
            field=models.UUIDField(default=uuid.UUID('4635d13c-1b4c-4c69-b542-8cd2757eff04'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 21, 7, 48, 7, 292748, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ingredientdbmodel',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 21, 7, 48, 7, 292748, tzinfo=datetime.timezone.utc)),
        ),
    ]
