import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from products.models import (
    Product, 
    Color, 
    Size,
    Menu,
    Category
)

CSV_PATH_PRODUCTS = './spao.csv'

with open(CSV_PATH_PRODUCTS) as in_file :

    data_reader = csv.reader(in_file)
    
    next(data_reader,None)

    for row in data_reader :
        
        if row[0] :
            color_name=row[0]
            Color.objects.create(name=color_name)
        
        if row[1] :
            size_name = row[1] 
            Size.objects.create(name=size_name)

        if row[3] :
            product_name = row[3]
        
        if row[4] :
            menu_name = row[4]
            menu_id   = Menu.objects.get(name=menu_name).id
        
        if row[5] :
            category_name = row[5]
            category_id  = Category.objects.get(menu_id=menu_id, name=category_name).id
        
        if row[6] :
            price = row[6]
        
        if row[7] :
            description = row[7]
        
        if row[8] :
            quantity = row[8]
        
        if row[9] :
            thumbnail = row[9]
            Product.objects.create(name=product_name, menu_id=menu_id, category_id=category_id ,price=price, description=description, quantity=quantity, thumbnail=thumbnail)