#Kimptch App
from django.contrib import admin
from .models import *

#Only lenders' model.
admin.site.register(Lender)