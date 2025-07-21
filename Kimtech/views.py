#Kimtech Views

from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import HttpResponse
from .models import *
from .logic import exp_check

# Create your views here.


def index(request):
    print('\n\n======>>>>>Someone have accessed index page!\n\n')
    #Login logic here.
    return render(request, 'index.html')

#VIEW AVAILABLE LENDERS
def lenders(request):
    exp_check()
    lender = Lender.objects.all()
    return render(request, 'lenders.html', {'lender':lender})
    
    
#OPEN/ Create lender account
def create_account(request):
    
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        co_name = request.POST.get('co_name')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        username = request.POST.get('uname')
        password = request.POST.get('pw')
        location = request.POST.get('location')
        try:
            Lender.objects.create(
                logo = logo,
                co_name = co_name, 
                tel = tel, email = email, 
                username =username, 
                password = password, 
                location = location, 
                subscription = True,
                subscription_status = 'Trial'
             )#Expiry is added automatically
            exp_check()
            request.session['uname'] = username
            print('\n\n=====>>SAVED lender SUCCESSFULLY\n\n')
            lender = Lender.objects.get(username = username)
            return render(request, 'dashboard.html', {'lender' : lender})
            
        except IntegrityError as e:
            print('===>Exception : ', e)
            lender = Lender.objects.all()
            return render(request, 'lenders.html', {'lender':lender, 'ex':e, 'uname':username })#
    lender = Lender.objects.all()#
    return render(request, 'lenders.html', {'lender':lender})#
    
    
def admin(request):
    lenders = Lender.objects.all()
    total = 0
    active = 0
    trial = 0
    for l in lenders:
        total += 1
        if l.subscription == True:
            active += 1
            if l.subscription_status == 'Trial':
                trial += 1
                
    summary = {
        'lenders' : lenders,
        'total' : total,
        'active' : active,
        'trial' : trial,
        'expired' : total - active,
    }
    return render(request, 'admin.html', summary)