import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spao.settings")

django.setup()

from users.models import User

CSV_PATH_USERS = './user_csv.csv'

with open(CSV_PATH_USERS) as in_file:
    
    data_reader = csv.reader(in_file)
    
    next(data_reader, None)
    
    for row in data_reader:
            
        if row[1]:
             username=row[1]
        
        if row[2]:
              password =row[2]
             
        if row[3]:
              name = row[3]
              
        if row[4]:
              email = row[4]
               
        if row[5]:
              mobile_number = row[5]
        if row[6]:
              address1 = row[6]
        if row[8]:
              birthday = row[8]
        User.objects.create(
            username = username,
            password = password,
            name = name,
            email = email,
            mobile_number = mobile_number,
            address1 = address1,
            birthday = birthday
        )