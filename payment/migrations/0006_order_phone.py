# Generated by Django 4.2.5 on 2024-06-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_shippingaddress_shipping_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
