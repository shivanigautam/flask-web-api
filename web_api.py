from flask import Flask, jsonify
from flask import request
from datetime import date, datetime

from PaymentMethod import PaymentMethod
from UserHistory import UserHistory

app = Flask(__name__)

@app.route("/")
def index():
    return "Hi, Welcome to Web API"

@app.route("/payment", methods=['POST', 'GET'])
def ProcessPayment():
    global result

    methodname  = PaymentMethod()
    userHistory = UserHistory()
    if request.method == 'POST':

        ### Validation of Card Number ######
        credCardNum = request.get_json().get('credit_card_number', '')
        lengthCredCard = len(credCardNum)

        if (credCardNum == ""):
            return "Credit Card Number is mendatory"
        if (lengthCredCard != 16):
            return "Credit Card Number Not Valid, Please provide valid card number"

        ### Validattion of Card Holder Name #####
        cardHolderName = request.get_json().get('card_holder', '')
        if (cardHolderName == ""):
            return "Card Holder Name is mendatory"

        ## Validation of Expiry Date of a Card #####
        # Returns the current local date
        today = date.today()
        today = str(today)
        expDate = request.get_json().get('expiration_date', '')

        oldDatedCard = datetime.strptime(today, '%Y-%m-%d')
        ValidCard = datetime.strptime(expDate, '%Y-%m-%d')

        if (ValidCard < oldDatedCard):
            return "Card Validity is Expired!"

        ### validate Security Code
        ##  optionaol parameter,
        ##  but if Security Code is available so its length must be 3
        secCode = request.get_json().get('security_code', '')
        secCodeLen = len(secCode)
        if (secCodeLen != 3) & (secCodeLen != 0):
            return "Security Code is Invalid!!!"

        amount = request.get_json().get('amount', '')

        # if amount is less thsan 20
        # so it will served by CHeap pyment gateway method
        if (amount <= 20):
            result = methodname.CheapPaymentGateWay()
            #result = CheapPaymentGateWay()
        ## if amount is in between below range so
        ## it will accessed by Expensive Payment Method
        elif (amount >= 21) & (amount <= 500):
            ## whether Expensive Method is available of not
            # if available then accessed by EXpensive Payment Method
            ## Otherwise it will processed only once with CheapPaymentMethod for one user
            if (ifAvailable()):
                result = methodname.ExpensivePaymentGateWay()
            else:
                ## save user data in userHistory Table
                userHistory.UpdateUserHistoryTable(cardHolderName, credCardNum)
                ## read value from userHistory Table
                value = userHistory.userHist(credCardNum, "expensive")
                if (value == 1):
                    result = methodname.CheapPaymentGateWay()
                    result = result + " Because Expensive Payment is not available, Caution You have used your limit due to Unavailable Expensive method"
                else:
                    return "Please after some time, Expensive method is not available at this time"
        else:
            ## save userHistory on 'premium' table
            userHistory.PremiumHistory(cardHolderName, credCardNum)
            ## read user history from 'premium' Table
            value = userHistory.userHist(credCardNum,"premium")
            ## only three tries is possibe for one user at a time
            if (value > 3):
                return "You have exhausted limit Of Premium Payment Method"
            else:
                result = methodname.PremiumPaymentGateWay()
        return result
    else:
        return jsonify(status_code=404, message="Method Not Allowed Here! Request is invalid")


## check Expensive Method is available or not
def ifAvailable():
    import datetime
    available = False

    #AS of now unavailabe of Expensive Payment Gateway Method is HARDCODED from 8PM to 10PM
    #Please avoid these time duration if you want to use Expensive Payment Gateway Method
    uprLimit = datetime.time(20, 00, 00)
    lowerLimit = datetime.time(22, 00, 00)

    currentTime = datetime.datetime.now()
    currentTime = currentTime.time()

    if (currentTime >= uprLimit) & (currentTime <= lowerLimit):
        available = True

    print(bool(available))

    ## if method is available so it returns TRUE
    # otherwise returns FALSE
    return available

if __name__ == '__main__':
    app.run(debug=True)
