from django.shortcuts import render, HttpResponse
from gateway import forms,models
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
from paymentGatewayPayTM.settings import MERCHANT_KEY


def userinfo(request):
    if request.method == 'GET':
        i_form = forms.InfoForm()
        context={
            'i_form':i_form
        }
        return render(request,'userinfo.html', context)
    elif request.method == 'POST':
        no = request.POST.get('no')
        name = request.POST.get('name')
        price = request.POST.get('price')
        i_model = models.InfoModel(no=no, name=name, price=price)
        i_model.save()

        #Req payTm to transfer amountto your account from user.
        param_dict = {

            'MID': 'DjaXIb90413122149989',
            'ORDER_ID': 'scsdfsdfsfsdkjjjj',
            'TXN_AMOUNT': '1',
            'CUST_ID': 'khajuria.saket486@gmail.com',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

