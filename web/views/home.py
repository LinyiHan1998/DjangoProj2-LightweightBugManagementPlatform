import datetime
import json
import paypalrestsdk
from django.conf import settings


import redis
from django.shortcuts import render, redirect
from utils.encrypt import uid
from web import models
def index(request):
    return render(request,'web/index.html')

def price(request):
    policy_list = models.PriceStrategy.objects.filter(category=2)
    return render(request,'web/price.html',{'policy_list':policy_list})

def payment(request,policy_id):
    #1.价格策略
    policy_obj = models.PriceStrategy.objects.filter(id=policy_id,category=2).first()
    if not policy_obj:
        return redirect('price')
    #2.要购买的数量
    number = request.GET.get('number','')
    if not number or not number.isdecimal():
        return redirect('price')
    number = int(number)
    if number < 1:
        return redirect('price')
    #3. 计算原价
    balance = 0
    origin_price = number * policy_obj.price
    #4. 之前购买过套餐
    if request.tracer.price_strategy.category == 2:
        _object = models.Transaction.objects.filter(userId=request.tracer.user,status=1).order_by('-id').first()
        total_timedelta = _object.validUntil - _object.startTime
        balance_timedelta = _object.validUntil - datetime.datetime.now()
        if total_timedelta == balance_timedelta:
            balance = _object.paidAmt / total_timedelta.days *(balance_timedelta.days - 1)
        else:
            balance = _object.paidAmt / total_timedelta.days * (balance_timedelta.days)
        print(_object)
    if balance >= origin_price:
        return redirect('price')
    context = {
        'policy_id':policy_obj.id,
        'number':number,
        'origin_price':origin_price,
        'balance':round(balance,2),
        'total_price':origin_price- round(balance,2)
    }
    r = redis.Redis(
        host='127.0.0.1',
        port=6379
    )
    key = 'payment_{}'.format(request.tracer.user.email)
    r.set(key, json.dumps(context), ex=60 * 30)
    context['policy_object'] = policy_obj

    return render(request,'web/payment.html',context)

def pay(request):
    ###generate order
    ###check user send info, in case user changed price
    r = redis.Redis(
        host='127.0.0.1',
        port=6379
    )
    key = 'payment_{}'.format(request.tracer.user.email)
    context_str = r.get(key)
    if not context_str:
        return redirect('price')
    context = json.loads(context_str.decode('utf-8'))

    #1. generate order, pending payment
    #2. update the transaction status start/end time when payment is finished
    orderId = uid(request.tracer.user.email)
    models.Transaction.objects.create(
        status=2,
        userId=request.tracer.user,
        price_strategy_id=context['policy_id'],
        paidAmt=context['total_price'],
        amtYear=context['number'],
        orderId=orderId,
    )
    starategy = models.PriceStrategy.objects.filter(id=context['policy_id']).first()
    paypalrestsdk.configure(settings.PAYPAL_CONF)
    #2. go to paypal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/index/",
            "cancel_url": "http://127.0.0.1:8000/index/"},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": starategy.title,
                    "sku": "item",
                    "price": starategy.price,
                    "currency": "USD",
                    "quantity": context['number']}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total":context['total_price'],
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
                return redirect(approval_url)
    else:
        print("Error while creating payment:")
        print(payment.error)
        url = ""
        return redirect(url)