#Kimtech urls

from django.urls import path
from . import views

app_name = 'kim'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('lenders', views.lenders, name = 'lenders'),
    path('create_account', views.create_account, name = 'create_account'),
    path('kimAdmin', views.admin, name = 'admin'),
]