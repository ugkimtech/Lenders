import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import requests
from Kimtech.models import *
import calendar


class NewLoan:
    def __init__(self, access):
        self.access = access
        self.lender = Lender.objects.get(username = self.access)
        
        
    def borrowerInfo(self, name, NIN, tel, email, location, pin, photo, chair,chairTel, nextOfKin, nextOfKinTel, buz, buzloc ):
        try:
            Borrower.objects.create(
                lender_id = self.lender,
                name = name,
                tel = tel,
                email = email,
                location = location,
                NIN = NIN,
                pin = pin,
                photo = photo,
                chair = chair,
                chairTel = chairTel, 
                nextOfKin = nextOfKin, 
                nextOfKinTel = nextOfKinTel, 
                buz = buz, 
                buzloc = buzloc
            )
            print('\n\n===>borrower info success for \n\n', self.lender.co_name)
            return True
        except Exception:
            print('\n\n===>Error occured on borrower info for ', self.lender.co_name)
            return False
            
            
    def loanInfo(self, nin, loan_amount, interest_rate, processing_fee, duration, startDate, comments, penalty, effectDay, dailyPay):
        borrower = Borrower.objects.get(lender_id = self.lender, NIN = nin)

        last_date = date.today() + timedelta(days = int(duration))
        total_amm = int(loan_amount) + int(processing_fee) + ( (float(interest_rate)/100) * int(loan_amount))
                
        try:
            Loans.objects.create(
                lender_id = self.lender,
                borrower_id = borrower,
                loan_amount = loan_amount,
                interest_rate = interest_rate,
                processing_fee = processing_fee,
                total_amm = total_amm,
                duration = duration,
                last_date = last_date,
                balance = total_amm,
                comments = comments,
                startDate = startDate,
                penalty = penalty,
                effectDay = effectDay
            )
            print('\n\n===>loan info success for \n\n', self.lender.co_name)
            return True
        except Exception:
            Borrower.objects.get(lender_id = self.lender, NIN = nin).delete()
            print('\n\n===>Error occured on loan info for \n\n', self.lender.co_name)
            return False
            
            
    def agreementInfo(self, nin, aggreement):
        borrower = Borrower.objects.get(lender_id = self.lender, NIN = nin)
        loan = Loans.objects.get(lender_id = self.lender, borrower_id = borrower)
        try:
            Aggreements.objects.create(
                lender_id = self.lender,
                borrower_id = borrower,
                loan_id = loan,
            aggreement = aggreement
            )
            print('\n\n===>Agreement info success for \n\n', self.lender.co_name)
            return True
        except Exception:
            Borrower.objects.get(lender_id = self.lender, NIN = nin).delete()
            print('\n\n===>Error occured on agreement info for \n\n', self.lender.co_name)
            return False
            
            
    def collateralInfo(self, nin, asset_name, description, proof, asset_photo):
        borrower = Borrower.objects.get(lender_id = self.lender, NIN = nin)
        loan = Loans.objects.get(lender_id = self.lender, borrower_id = borrower)
        aggreement = Aggreements.objects.get(lender_id = self.lender, borrower_id = borrower)
        try:
            Collateral.objects.create(
                lender_id = self.lender,
                borrower_id = borrower,
                loan_id = loan,
                aggr_id = aggreement,
                asset_name = asset_name,
                description = description,
                proof = proof,
                asset_photo = asset_photo
            )
            print('\n\n===>>  Collateral info success for \n\n', self.lender.co_name)
            return True
        except Exception:
            Borrower.objects.get(lender_id = self.lender, NIN = nin).delete()
            print('\n\n===>Error occured on collateral info for \n\n', self.lender.co_name)
            return False
            
            
class Statistics:
    def __init__(self, period):
        self.period = period
        print('===>', self.period)
        self.today = datetime.now()
        self.c_month_d = self.today.month
        self.time = self.c_month_d
        print('=****=>', self.time)
        
        if self.period == 1:
            self.c_month_d = self.today.month
            self.time = self.c_month_d
            print('=****=>', self.time)
            
        elif self.period == 2:
            self.p_month_d = self.today.month - 1
            self.time = self.p_month_d
            print('=****=>', self.time)
            
        else:
            self.time = ''
            print('=****=>', self.time)
        
    def getTotalLoans(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        print('\n\n=****=>', self.time)
        total = 0
        for l in loans:
            total = total+1
        return total
        
        
    def totalLoanAmount(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        total_amm = 0
        for l in loans:
            total_amm = total_amm + l.total_amm
        return total_amm
        
        
    def ptPaid(self, lender_id):
        paid = 0
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        for l in loans:
            paid += (l.total_amm - l.balance)
        try:
            paid_rate = (int(paid)/self.totalLoanAmount(lender_id)) * 100
        except ZeroDivisionError:
            paid_rate = 0
        return [paid, paid_rate]
        
        
    def fullPay(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        fully = 0
        count = 0
        for l in loans:
            if l.balance <= 0:
                count += 1
                fully += l.total_amm
        try:
            rate = (fully/self.totalLoanAmount(lender_id)) * 100
        except ZeroDivisionError:
            rate = 0
        return [count, rate, fully]
        
        
    def unpaid(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__contains = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        bal = 0
        rate = 0
        for l in loans:
            bal += l.balance
        try:
            rate = (bal/self.totalLoanAmount(lender_id)) * 100
        except ZeroDivisionError:
            rate = 0
        return [bal, rate]
        
        
    def interest(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        paid_so_far = 0
        interest = 0
        exp_intr = 0
        for l in loans:
            exp_intr += (l.total_amm - l.loan_amount) + l.penaltyAmountAdded
            paid_so_far = l.total_amm - l.balance
            if paid_so_far >= l.loan_amount:
                interest += (paid_so_far - l.loan_amount)
        try:
            rate = (interest/exp_intr) * 100
        except ZeroDivisionError:
            rate = 0
        return [exp_intr, interest, rate]
        
        
    def penalty(self, lender_id):
        try:
            loans = Loans.objects.filter(lender_id = lender_id, loan_Date__month = self.time)
        except Exception:
            loans = Loans.objects.filter(lender_id = lender_id)
            
        total = 0
        collected = 0
        for l in loans:
           total += l.penaltyAmountAdded
        return total
    
    
class Notifications:
    def sendNote(self):
        notif = [
            
        ]
        no = 0
        for n in notif:
            no+=1
        return [no, notif]
        
        
    def send_email(self, msg):
        try:
            send_mail(
                subject = 'NOTIFICATION FROM LMS',
                message=msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                        'ugkimtech@gmail.com',
                        'charleskim474@gmail.com'
                ],
                fail_silently=False,
            )
            print('mail sent')
        except Exception as e:
                print(e)
        
        
class Payments:
    def __init__(self, lender):
        self.lender = lender
        
        
    def pay(self, amm, network, tel, plan ):
        obj = Notifications()
        #generating reference
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        uuid_part = uuid.uuid4().hex[:6]
        txnRef = f"TXN-{uuid_part}-{timestamp}"
        try:
            Subscriber.objects.create(
                name = self.lender.co_name,
                username = self.lender.username,
                plan = plan,
                amm = amm,
                txnID = txnRef
            )
            print('\n\nTXN added to db\n\n')
        except Exception as e:
            print('\n\n', e)
        #To be replaced by api provider info
        #_____________________________________
        
        url = 'https://www.easypay.co.ug/api/'
        username = ''
        password = ''
        if network == 'Airtel':
            username = '22f16ffa430705e1'
            password = 'cb68419e05c52540'
        else:
            pass
            #MTN credentials
            #username = '22f16ffa430705e1'
            #password = 'cb68419e05c52540'
        
        payload = {
            "username": username,
            "password": password ,
            "action":"mmdeposit",
            "amount": amm,
            "currency":"UGX",
            "phone": tel,
            "reference": txnRef,
            "reason":"Payment for system activation"
        }
        #_______________________________
        try:
            response = requests.post(url, json = payload)
            if response.status_code == 200:
                print('\n\n Request status',response.json(), '\n\n')
                data = response.json()
                if data['success'] == 1:
                    obj.send_email(f"Received UGX {data['details']['amount']} from :  {data['details']['phone']} Ref :  {data['details']['reference']} TXN ID : {data['details']['transactionId'] }")
                    return True
                else:
                    obj.send_email(f"Payment of {amm} from {tel} unsuccessfull (code: 200)")
                    return False
            else:
                print('\n\nRequest failed',response.json(),'\n\n')
                obj.send_email(f"Payment of {amm} from {tel} unsuccessfull (code: != 200)")
                return False
        except Exception as e:
            print('\n\n API request Exeption', e, '\n\n')
            return False
            
            
class Update:
    def __init__(self, lender):
        self.subscriber = lender
        self.lender = Lender.objects.get(username = self.subscriber.username)
        
        
    def activate(self, plan):
        expiry = self.lender.expiry + timedelta(days = int(plan))
        time_left = self.lender.time_left + (expiry - date.today()).days
        #update changes
        self.lender.subscription = True
        self.lender.subscription_status = 'Working'
        self.lender.expiry = expiry
        self.lender.time_left = time_left
        self.lender.save()
        return
    
# Give chance to send error msg without login.
class UnkownUser:
    id = '< Not Registered >'
    co_name = '< Not Registered >'
    username = '< Not Registered >'