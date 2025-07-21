#Logic In Kimtech
from .models import Lender, Loans, Repayment
from datetime import date, timedelta, datetime
from decimal import Decimal

#SUBSCRIPTIONS

#Check status
def exp_check():
    lender_check = Lender.objects.all()
    for l in lender_check:
        exp = l.expiry
        if exp >= date.today():
            Lender.objects.filter(id = l.id).update(subscription = True) #
            t_left = exp - date.today()#
            Lender.objects.filter(id = l.id).update(time_left = t_left.days)#
        else:
            Lender.objects.filter(id = l.id).update(subscription = False)#
            Lender.objects.filter(id = l.id).update(subscription_status = 'Working')#
            Lender.objects.filter(id = l.id).update(time_left = -1)###
    loan = Loans.objects.all()
    for l in loan:
        time_left = l.last_date - date.today()
        Repayment.objects.filter(loan_id = l.id).update(time_left = time_left.days)
        
        
    #TO CHECK FOR LATE REPAYMENTS
    loans = Loans.objects.filter()
    for loan in loans:
        today = (datetime.today() -  datetime(1970, 1, 1)).days
        lastDate = (loan.last_date - date(1970, 1, 1)).days
        
        if (today - loan.effectDay) > lastDate:
            newExpiry = date.today() + timedelta(days = loan.duration)
            newBalance = loan.balance + ( (Decimal(loan.penalty) / 100) * loan.balance)
            loan.penaltyAmountAdded = (Decimal(loan.penalty) / 100) * loan.balance
            loan.last_date = newExpiry
            loan.balance = newBalance
            loan.save()  # Save the changes to the database
            print('\n\n====>Penalty Added seccessfuly in lender: ', loan.lender_id.co_name)
        else:
            print('\n\n====>No penalty found but seccessfuly checked for lender: ', loan.lender_id.co_name)