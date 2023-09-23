from utils import Bootstrap
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.core.validators import RegexValidator
from django.views.decorators.csrf import csrf_exempt
from utils.aws.awsSNS import SnsWrapper
from utils.encrypt import md5
from web import models
import redis

class RegisterModelForm(Bootstrap.BootstrapModelForm):
    mobile_phone = forms.CharField(label='Mobile Phone',validators=[RegexValidator('^(\\+)?([1])\\d{10}$','invalid number'),])
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())
    code = forms.CharField(label='Verify Code')
    class Meta:
        model = models.UserInfo
        fields = ['username','password','confirm_password','email','mobile_phone','code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Please type in %s'%(field.label,)
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm :
            raise ValidationError("Password doesn't mach")
        return confirm
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email)
        if exists:
            raise ValidationError('Account already exists')
        return email
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

class SmsForm(Bootstrap.BootstrapForm):
    email = forms.CharField(label='email',validators=[RegexValidator('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$','Invalid Email'),])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('Email already exist')
        return email

class LoginSmsForm(Bootstrap.BootstrapForm):
    email = forms.CharField(label='email',validators=[RegexValidator('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$','Invalid Email'),])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email).exists()
        if not exists:
            raise ValidationError('Email does not exists')
        return email
class LoginForm(Bootstrap.BootstrapForm):
    bootstrap_class_exclude = ['code']
    email = forms.CharField(label='Email', validators=[RegexValidator('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', 'Invalid Email'), ])
    #code = forms.CharField(label='Verify Code',widget=forms.TextInput())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        exists = models.UserInfo.objects.filter(email = email).exists()
        if not exists:
            raise ValidationError("Email doesn't exists")
        return email
    # def clean_code(self):
    #     r = redis.Redis(
    #         host='127.0.0.1',
    #         port=6379
    #     )
    #     if self.cleaned_data.get("email") is None:
    #         raise ValidationError("Email does not exists")
    #     code = str(r.get(self.cleaned_data.get("email")), 'utf-8')
    #     print(self.cleaned_data.get("code"))
    #     print(code)
    #     if code != self.cleaned_data.get("code"):
    #         raise ValidationError("Code doesn't match")
    #     return self.cleaned_data.get("code")


class LoginUserForm(Bootstrap.BootstrapForm):
    bootstrap_class_exclude = ['code']
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    #code = forms.CharField(label='Verify Code', widget=forms.TextInput())

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = md5(self.cleaned_data.get("password"))

        return pwd

    # def clean_code(self):
    #     code = self.cleaned_data.get("code")
    #     session_code = self.request.session["image_code"]
    #     if not session_code:
    #         raise ValidationError("Code expired")
    #     if code.strip().upper() != session_code.strip().upper():
    #         raise ValidationError("Incorrect Code")
    #     return code