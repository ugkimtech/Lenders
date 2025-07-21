#Lender_Admin App
from django.contrib import admin
from Kimtech.models import *

# All lenders' info.
admin.site.register(Borrower)
admin.site.register(Loans)
admin.site.register(Repayment)
admin.site.register(Aggreements)
admin.site.register(Collateral)