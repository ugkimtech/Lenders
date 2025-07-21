#Lenders Admin Views
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Kimtech.models import *
from datetime import date, timedelta
from Kimtech.logic import exp_check
from .logic import *
from .logic import Statistics


#LOGIN FOR LENDER

def login(request):
    exp_check()
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pw = request.POST.get('pw')
        try:
            row = Lender.objects.get(username = uname)
        except Lender.DoesNotExist as e:
            request.session['uname'] = uname
            request.session['pw'] = pw
            return redirect('app:status')
        if row and row.password == pw:
            request.session['uname'] = uname
            print(f"===Added : {request.session.get('uname', 'Sessiom Not Added')} to session")
            if row.subscription == False:
                messages.success(request, f'Dear customer, your subscription expired on {row.expiry}! \n Please subscribe and gain full access to your data.')
                return redirect('app:subscription')
            else:
                return redirect('app:home')
        else:
            return render(request, 'index.html', {'msg':'Invalid Username or Password, please try again!'})
    return render(request, 'index.html')


def home(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        row = Lender.objects.get(username = access)
        note = Notifications()
        notifications = note.sendNote()
        return render(request, 'dashboard.html', {'lender' : row, 'count' : notifications[0], 'notifications' : notifications[1]})
    else:
        return redirect('app:login')


#Logout FOR ALL
def logout(request):
    exp_check()
    request.session.flush()
    return redirect('app:login')



#REGISTER BORROWERS & all loan info

def add_borrower(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            print('===>Loged in with ',access)
            if request.method == 'POST':
                lender = Lender.objects.get(username = access)
                save = NewLoan(access)
            
                #Borrower details
                name = request.POST.get('name')
                tel = request.POST.get('tel')
                email = request.POST.get('email')
                location = request.POST.get('location')
                chair = request.POST.get('chair')
                chairTel = request.POST.get('chairTel')
                nextOfKin = request.POST.get('nextOfKin')
                nextOfKinTel = request.POST.get('nextOfKinTel')
                buz = request.POST.get('buz')
                buzloc = request.POST.get('buzloc')
                pin = request.POST.get('pin')
                photo = request.FILES.get('photo', '/static/images/blankPerson.jpeg')
                NIN = request.POST.get('NIN')
                try:
                    NINcheck = Borrower.objects.get(lender_id = lender, NIN = NIN)
                    if NINcheck.NIN == NIN:
                        print('===>>Identical NIN found')
                        return render(request, 'new_borrower.html', {'NINerr':'NIN already used In this Company!'})
                except Borrower.DoesNotExist:
                    print('===>>No Identical NIN found')
            
                if save.borrowerInfo(name, NIN, tel, email, location, pin, photo, chair,chairTel, nextOfKin, nextOfKinTel, buz, buzloc):
                    #Loan Details
                    loan_amount = request.POST.get('loan_amount')
                    interest_rate = request.POST.get('interest_rate')
                    processing_fee = request.POST.get('processing_fee')
                    duration = request.POST.get('duration')
                    startDate = request.POST.get('date')
                    comments = request.POST.get('comments')
                    penalty = request.POST.get('penalty')
                    effectDay = request.POST.get('effectDay')
                    dailyPay = request.POST.get('dailyPay')
                    nin = NIN# for extracting borrower info
                    if save.loanInfo(nin, loan_amount, interest_rate, processing_fee, duration, startDate, comments, penalty, effectDay, dailyPay):
                        #Agreement
                        aggreement = request.FILES.get('aggreement', '/static/images/blankPerson.jpeg')
                        if save.agreementInfo(nin, aggreement):
                            #Collateral
                            asset_name = request.POST.get('asset_name')
                            description = request.POST.get('description')
                            proof = request.FILES.get('proof')
                            asset_photo = request.FILES.get('asset_photo')
                            if save.collateralInfo(nin, asset_name, description, proof, asset_photo):
                                #when everything is added successfuly
                                return redirect('app:loans')
                            else:
                                return render(request, 'new_borrower.html', {'msg': 'Error occured in Collateral Information check for mistakes and try again. '})
                        else:
                            return render(request, 'new_borrower.html', {'msg': 'Error occured in Agreement Information check for mistakes and try again. '})
                    else:
                        return render(request, 'new_borrower.html', {'msg': 'Error occured in Loan Information check for mistakes and try again. '})
                else:
                    return render(request, 'new_borrower.html', {'msg': 'Error occured in Borrower Information check for mistakes and try again. '})
            else:
                lender = Lender.objects.get(username = access)
                return render(request, 'new_borrower.html', {'lender' : lender } )
    else:
        return redirect('app:login')
        

#VIEW BORROWERS (Lender based after login) WITH ALL LOANS

def customers(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            lender_id = lender.id
            loan = Loans.objects.filter(lender_id = lender_id)
            print('===>', access)#....
            today = date.today()
           # today = today.days
            return render(request, 'customers.html', {'loan':loan, 'today': today, 'lender': lender })
    return redirect('app:login')


#RETURNS ALL LOANS OF A LENDER
def loans(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            lender_id = lender.id
            loans = Loans.objects.filter(lender_id = lender_id)
            print('===>', access)#...
            today = date.today()
            return render(request,'loans.html', {'loans': loans, 'lender': lender, 'today':today})
    return redirect('app:login')



#Repayments RECORDS REPAYMENTS & RETURNS THE REPAYMENTS LIST
def repayments(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            if request.method == 'POST':
            #select name from drop down list
                borrower_id = request.POST.get('id')
                paid = request.POST.get('paid')
                borrower = Borrower.objects.get(id = borrower_id, lender_id = lender)
                loan = Loans.objects.get(lender_id = lender, borrower_id = borrower)
                loan.total_amm
                bal = loan.balance - int(paid)
                try:
                    percentage_paid = 100 - ( ( bal/loan.total_amm ) * 100 )
                except ZeroDivisionError:
                    percentage_paid = 100
                    print('Zero Division Error!')
                time_left = loan.last_date - date.today()
                Repayment.objects.create(
                    lender_id = lender,
                    borrower_id = borrower,
                    loan_id = loan,
                    paid = paid,
                    percentage_paid = percentage_paid,
                    bal = bal,
                    time_left = time_left.days
                )
                #
                loan = Loans.objects.get(lender_id = lender, borrower_id = borrower)
                loan.balance = bal
                loan.save()  # Save the changes to the database
                
                print('====> Repayment added for ', loan.borrower_id.name)
                repayments = Repayment.objects.filter(lender_id = lender)
                loans = Loans.objects.filter(lender_id = lender)
                return render(request, 'repayments.html',{'repayments': repayments, 'pay':'pay', 'loans':loans, 'lender': lender})
            repayments = Repayment.objects.filter(lender_id = lender)
            loans = Loans.objects.filter(lender_id = lender)
            return render(request, 'repayments.html',{'repayments': repayments, 'pay':'pay', 'loans':loans, 'lender': lender})# loans provide drop down list
    return redirect('app:login')
    
#Aggreements & collateral information
def aggreements(request):
    exp_check()
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            #use collateral model to get all required information
            collateral = Collateral.objects.filter(lender_id = lender)
            return render(request, 'aggreements.html', {'info': collateral, 'lender': lender})
    return redirect('app:login')


#Borrower access
def status(request):
        user = request.session.get('uname')
        password = request.session.get('pw')
        try:
            customer = Borrower.objects.get(NIN = user, pin = password)
            if customer.NIN == user and customer.pin == password:
                print('===>>>Customer added to session ', customer.name)
                try:
                    data = Collateral.objects.get(lender_id = customer.lender_id, borrower_id = customer)
                    repayments = Repayment.objects.filter(lender_id = customer.lender_id, borrower_id = customer)
                    Ldate = Loans.objects.get(borrower_id = customer)
                    tLeft = (Ldate.last_date - date.today()).days
                    return render(request, 'info.html', {'data':data, 'info':repayments, 'tLeft' : tLeft})
                except Exception:
                    print('===>No collateral info found')
                    return HttpResponse('<h1>Missing Information In The System, Please Contact your Lender For Assistance! <br />Thank you.</h1>')
                    #return error page
            return render(request, 'index.html', {'msg':'Invalid Username or Password, please try again!'})
        except Borrower.DoesNotExist:
            return render(request, 'index.html', {'msg':'Invalid Username or Password, please try again!'})
            
            
def statistics(request):
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            period = 1
            if request.method == 'POST':
                period = int(request.POST.get('period', 3))
                
            if period == 1:
                time = "This Month"
            elif period == 2:
                time = "Last Month"
            else:
                time = "All"
                
            stat = Statistics(period)
            statistics = {
                'time' : time,
                'logo' : lender.logo,
                'name' : lender.co_name,
                'total_loans' : stat.getTotalLoans(lender),
                'total_amm' : stat.totalLoanAmount(lender),
                'part_paid' : stat.ptPaid(lender)[0],
                'ptPaid_rate' : stat.ptPaid(lender)[1],
                'success_loans' : stat.fullPay(lender)[0],
                'rate' : stat.fullPay(lender)[1],
                'success_pay' : stat.fullPay(lender)[2],
                'loan_balance' : stat.unpaid(lender)[0],
                'bal_rate' : stat.unpaid(lender)[1],
                'exp_interest' : stat.interest(lender)[0],
                'collected_intr' : stat.interest(lender)[1],
                'intr_rate' : stat.interest(lender)[2],
                'penalty' : stat.penalty(lender)
                #Graph data
            }
            
            
            
            return render(request, 'statistics.html', statistics)
    return redirect('app:login')
    
    
def profile(request):
    access = request.session.get('uname', 'deny')
    if access != 'deny':
        lender = Lender.objects.get(username = access)
        if lender.subscription == False:
            messages.success(request, f'Dear customer, your subscription expired on {lender.expiry}! \n Please subscribe and gain full access to your data.')
            return redirect('app:subscription')
        else:
            if request.method == 'POST':
                name = request.POST.get('co_name')
                tel = request.POST.get('tel')
                email = request.POST.get('email')
                location = request.POST.get('location')
                
                lender.co_name = name
                lender.tel = tel
                lender.email = email
                lender.location = location
                lender.save() 
            lender = Lender.objects.get(username = access)
            print('====> Updated to  ', lender)
            return render(request, 'profile.html', {'lender': lender} )
    return redirect('app:login')
    
    
def report_error(request):
    user = request.session.get('uname', 'deny')
    try:
        lender = Lender.objects.get(username = user)
    except Lender.DoesNotExist:
        print('Unknown Lender Submitting Error message')
        lender = UnkownUser()
        
    message = ''
    if request.method == 'POST':
        error_message = request.POST.get('error', '').strip()
        if error_message:
            try:
                send_mail(
                    subject = f'Error Report from {lender.co_name} U-Name: {lender.username}   User ID {lender.id}',
                    message=error_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[
                        'ugkimtech@gmail.com',
                        'charleskim474@gmail.com'
                    ],
                    fail_silently=False,
                )
                print('reported')
                msg = "Your error report has been sent. Thank you!"
                return render(request, 'report.html', {'msg': msg, 'lender' : lender})
            except Exception:
                return render(request, 'report.html', { 'lender' : lender, 'msg' : 'No Network Connection!'})
    return render(request, 'report.html', { 'lender' : lender})
    
         
def subscription(request):
    user = request.session.get('uname', 'deny')
    if user != 'deny':
        lender = Lender.objects.get(username = user)
        if request.method == 'POST':
            plan = request.POST.get('plan')
            pAmm = request.POST.get('pAmm')
            network = request.POST.get('network')
            phone = request.POST.get('tel')
            print('\n\n===> Request from id:',lender.id, '\nPlan : ', plan, '\nAmount : ', pAmm, '\nNetwork : ', network,  '\nTel : ', phone)
            #API logic
            subscribe = Payments(lender)
            confirm = subscribe.pay(pAmm, network, phone, plan)
            if confirm:
                #this may get handled direct from the hook
                obj = Update(lender)
                obj.activate(plan)
                print('\n\nWaiting for Validation \n\n')
                ##..........___________________,,,
                return redirect('app:home')
            else:
                return render(request, 'subscription.html', {'msg' : 'Error Occured! please try again or check your acount balance and try again.'})
        return render(request, 'subscription.html')
    return redirect('app:login')
 
 
@csrf_exempt
def webhook(request):
    obj = Notifications()
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("\n\nReceived webhook data:==>", data)
            #SUBSCRIPTION LOGIC HERE
            if data['success'] == 1:
                print("\n\nPaid successfully:==>", data)
                obj.send_email('Payment processed successfully')
            else:
                obj.send_email('Payment not processed processed')
            #____________________________
            return JsonResponse({"status": "success", "message": "Webhook received"}, status=200)
        except json.JSONDecodeError:
            obj.send_email('Payment not processed processed,  Invalid JSON payload! ')
            print("\n\nInvalid JSON payload! ")
            return JsonResponse({"status": "error", "message": "Invalid JSON payload"}, status=400)
    print("\n\nHttp method not allowed! ")
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)