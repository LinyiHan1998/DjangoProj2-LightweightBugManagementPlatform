import random
import redis
import boto3
import json
import uuid
import datetime

from io import BytesIO
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import HttpResponse,render,redirect
from django.db.models import Q
from web.forms.account import RegisterModelForm, SmsForm, LoginForm, LoginSmsForm, LoginUserForm
from django.views.decorators.csrf import csrf_exempt
from utils.aws.awsSNS import SnsWrapper
from utils.code import check_code
from web import models

from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register(request):
    if request.method =='GET':
        form = RegisterModelForm()
        return render(request,'web/register.html',{'form':form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        instance = form.save()
        price_policy = models.PriceStrategy.objects.filter(category=1,title='Free').first()
        models.Transaction.objects.create(
            status=1,
            userId=instance,
            price_strategy=price_policy,
            paidAmt=0,
            startTime=datetime.datetime.now(),
            amtYear=0,
            orderId=str(uuid.uuid4()),
        )
        return JsonResponse({'status':True,'data':'/login/username'})
    data_dict = {
        'status':False,
        'error':form.errors
    }
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return HttpResponse(json_string)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def send_sms(request):
    print(request.GET.get('email'))
    form = SmsForm(data=request.GET)
    print(form.is_valid())
    if form.is_valid():
        code = str(random.randint(10000000,99999999))
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.REGION_NAME
        )
        sns_wrapper = SnsWrapper(session.resource("sns"))
        topic = sns_wrapper.sns_resource.create_topic(Name="RequirementTacer")
        # topic_name = "RequirementTacer"
        print(code)
        text_send = sns_wrapper.publish_message(topic, code,{"key":'str'})
        r = redis.Redis(
            host = '127.0.0.1',
            port=6379
        )
        email = request.GET.get('email')
        r.set(email,code,60)
        return JsonResponse({'status':True})
    data_dict = {
        'status':False,
        'error':form.errors
    }
    return JsonResponse(data_dict)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def login_send_sms(request):
    print(request.GET.get('email'))
    form = LoginSmsForm(data=request.GET)
    print(form.is_valid())
    if form.is_valid():
        code = str(random.randint(10000000,99999999))
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.REGION_NAME
        )
        sns_wrapper = SnsWrapper(session.resource("sns"))
        topic = sns_wrapper.sns_resource.create_topic(Name="RequirementTacer")
        # topic_name = "RequirementTacer"
        print(code)
        text_send = sns_wrapper.publish_message(topic, code,{"key":'str'})
        r = redis.Redis(
            host = '127.0.0.1',
            port=6379
        )
        email = request.GET.get('email')
        r.set(email,code,60)
        return JsonResponse({'status':True})
    data_dict = {
        'status':False,
        'error':form.errors
    }
    return JsonResponse(data_dict)

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_sms(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'web/login_sms.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        email=form.cleaned_data['email']
        user_obj = models.UserInfo.objects.filter(email=email).first()
        request.session["user_id"] = user_obj.id
        request.session.set_expiry(60 * 60 * 24 * 7)
        return JsonResponse({'status':True,'data':'/register/'})
    return JsonResponse({'status':False,'error':form.errors})

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method =='GET':
        form = LoginUserForm(request)
        return render(request,'web/login.html',{'form':form})
    form = LoginUserForm(request,data= request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_obj = models.UserInfo.objects.filter(Q(email=username)|Q(username=username)).filter(password=password).first()
        print(user_obj)
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60*60*24*7)
            return redirect('/index/')
        form.add_error('username','incorrect username and password')
    return render(request,'web/login.html',{'form':form})

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def image_code(request):
    image_obj,code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_obj.save(stream,'png')


    return HttpResponse(stream.getvalue())

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def logout(request):
    request.session.flush()
    return redirect('index')