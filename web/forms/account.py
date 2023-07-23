from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.core.validators import RegexValidator
from django.views.decorators.csrf import csrf_exempt

from app01.utils.aws.awsSNS import SnsWrapper
from web import models
import redis

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
        code = str(r.get(self.cleaned_data.get("email")),'utf-8')
        print(self.cleaned_data.get("code"))
        print(code)
        if code != self.cleaned_data.get("code"):
            raise ValidationError("Code doesn't match")
        return self.cleaned_data.get("code")

class SmsForm(forms.Form):
    email = forms.CharField(label='email',validators=[RegexValidator('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$','Invalid Email'),])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('Email already exist')
        return email
