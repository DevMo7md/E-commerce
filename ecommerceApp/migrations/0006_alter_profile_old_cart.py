# Generated by Django 4.2.5 on 2024-06-14 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0005_profile_old_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
