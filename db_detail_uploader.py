import os
import django
import csv
import sys

from django.db import transaction
from db_uploader import CSV_PATH_PRODUCTS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from products.models import (
    DetailedProduct
)

CSV_PATH_PRODUCTS = './detail_product.csv'
with transaction.atomic() :
    with open(CSV_PATH_PRODUCTS) as in_file :
        data_reader = csv.reader(in_file)
        next(data_reader,None)
        
        bulk_list=[]
        
        for row in data_reader:
            # if row[0]:
            #     product_id = row[0]
                
            # if row[1]:
            #     color_id = row[1]
            
            # if row[2]:
            #     size_id = row[2]

            
            bulk_list.append(DetailedProduct(product_id=row[0], color_id=row[1], size_id=row[2]))
                    
        DetailedProduct.objects.bulk_create(bulk_list)