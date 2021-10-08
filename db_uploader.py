import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from products.models import Menu, Category, Product, Color, Size

CSV_PATH_PRODUCTS = './spao_data.csv'

with open(CSV_PATH_PRODUCTS) as in_file :

    data_reader = csv.reader(in_file)
    
    next(data_reader,None)

    for row in data_reader :
        
        if row[1] :
            menu_name=row[1]
            Menu.objects.create(name=menu_name)
        
        if row[2] :
            category_name = row[2]
            Category.objects.create(name=category_name, menu_id=Menu.objects.get(name=menu_name).id)

        if row[3] :
            product_name = row[3]
        
        if row[4] :
            price = row[4]
        
        if row[5] :
            description = row[5]
        
        if row[6] :
            quantity = row[6]
            Product.objects.create(name=product_name, price=price, description=description, quantity=quantity)

        if row[7] : 
            color_name = row[7]
            Color.objects.create(name=color_name)

        if row[8] :
            size_name = row[8] 
            Size.objects.create(name=size_name)