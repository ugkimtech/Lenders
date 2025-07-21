from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('login', views.login, name = 'login'),
    path('add_borrower', views.add_borrower, name = 'add_borrower'),
    path('customers', views.customers, name = 'customers'),
    path('loans', views.loans, name = 'loans'),
    path('repayments', views.repayments, name = 'repayments'),
    path('logout', views.logout, name = 'logout'),
    path('aggreements', views.aggreements, name = 'aggreements'),
    path('status', views.status, name = 'status'),
    path('home', views.home, name = 'home'),
    path('statistics', views.statistics, name = 'statistics'),
    path('profile', views.profile, name = 'profile'),
    path('report_error', views.report_error, name = 'report_error'),
    path('subscription', views.subscription, name = 'subscription'),
    path("webhook", views.webhook, name="webhook"),
]