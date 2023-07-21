import boto3
import redis
import json
import random
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.core.validators import RegexValidator
from django.views.decorators.csrf import csrf_exempt

from app01.utils.aws.awsSNS import SnsWrapper

from app01 import models
# Create your views here.
class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='Mobile Phone',validators=[RegexValidator('^(\\+)?([1])\\d{10}$','invalid number'),])
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    code = forms.CharField(label='Verify Code')
    class Meta:
        model = models.UserInfo
        fields = ['username','password','confirm_password','email','mobile_phone','code']
    def clean_confirm_password(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise ValidationError("Password doesn't mach")
        return self.cleaned_data.get("confirm_password")
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Please type in %s'%(field.label,)

    def clean_code(self):
        r = redis.Redis(
            host='127.0.0.1',
            port=6379
        )
        code = r.get(self.cleaned_data.get("email"))
        print(self.cleaned_data.get("code")[0])
        if code != self.cleaned_data.get("code")[0]:
            raise ValidationError("Code doesn't match")
        return self.cleaned_data.get("code")
@csrf_exempt
def send_sms(request):
    print(request.POST)
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
    email = request.POST.get('email')
    r.set(email,code,60)
    return HttpResponse('...')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request,'register.html',{'form':form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        print(form.is_valid())
        return JsonResponse({'status':True})
    data_dict = {
        'status':False,
        'error':form.errors
    }
    print(request.POST)
    print(form.errors)
    print(data_dict)
    json_string = json.dumps(data_dict, ensure_ascii=False)
    return HttpResponse(json_string)


