# Generated by Django 3.2 on 2022-06-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_food_avg_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]