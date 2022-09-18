# Generated by Django 3.2 on 2022-06-07 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_order_orderdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='food',
        ),
        migrations.RemoveField(
            model_name='order',
            name='food_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_charge',
        ),
        migrations.RemoveField(
            model_name='order',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='total_product',
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=0, null=True, verbose_name='Total Amount'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_product',
            field=models.IntegerField(default=0, null=True, verbose_name='Total Product'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.food'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='food_name',
            field=models.CharField(blank=True, help_text='Food Name', max_length=150, null=True, verbose_name='Food Name'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Food Price'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='quantity',
            field=models.FloatField(blank=True, null=True, verbose_name='Quantity'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='shipping_charge',
            field=models.FloatField(default=0, null=True, verbose_name='Shipping Charge'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='product.order'),
        ),
    ]
