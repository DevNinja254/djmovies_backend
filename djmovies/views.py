from members.models import DepositHistory, Profile, Paying, Paymentcode, Member
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def stkCallback(request):
    print("paid done...")
    callback_data = json.loads(request.body)
    # print(callback_data)
    response = callback_data['response']
    if callback_data["status"]:
        print("status true and code added")
        Paymentcode.objects.create(
            code = response['MpesaReceiptNumber'],
            amount = response["Amount"]
        )  
        try :
            paymentwaiting = Paying.objects.get(phone_number = response["Phone"])
            paymentExist = True
        except Paying.DoesNotExist:
            paymentExist = False

        if paymentExist:
            print("payment exist")
            userAccount = Profile.objects.get(buyerid = paymentwaiting.username)
            userAccount.account = int(userAccount.account) + response["Amount"]
            DepositHistory.objects.create(
                amount = response["Amount"],
                name = userAccount.user
            )
            userAccount.save()
            print("saved")
            paymentwaiting.delete() 
    # Return a success response to the M-Pesa server
    response_data = {"statement": "Payment statement received"}
    return JsonResponse(response_data, status=200)