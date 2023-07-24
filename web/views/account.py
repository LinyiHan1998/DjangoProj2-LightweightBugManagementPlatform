import random
import redis
import boto3
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import HttpResponse,render
from web.forms.account import RegisterModelForm, SmsForm, LoginForm, LoginSmsForm
from django.views.decorators.csrf import csrf_exempt
from utils.aws.awsSNS import SnsWrapper


@csrf_exempt
def register(request):
    if request.method =='GET':
        form = RegisterModelForm()
        return render(request,'web/register.html',{'form':form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status':True,'data':'/login/'})
    data_dict = {
        'status':False,
        'error':form.errors
    }
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return HttpResponse(json_string)

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

@csrf_exempt
def login_sms(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'web/login_sms.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        return JsonResponse({'status':True,'data':'/register/'})
    return JsonResponse({'status':False,'error':form.errors})