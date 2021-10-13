# Generated by Django 3.2.8 on 2021-10-12 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_thumbnail_product_thumbnail_image_url'),
        ('orders', '0003_alter_basket_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_color', to='products.detailedproduct'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_size', to='products.detailedproduct'),
        ),
    ]