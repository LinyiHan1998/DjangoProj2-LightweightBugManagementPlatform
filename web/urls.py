from django.conf.urls import url,include
from web.views import account

urlpatterns = [
    url(r'^register/', account.register, name='register'),
    url(r'^login/sms/', account.login_sms, name='login_sms'),
    url(r'^login/username', account.login, name='login'),
    url(r'^image/code', account.image_code, name='image_code'),
    url(r'^send/sms/', account.send_sms, name='send_sms'),
    url(r'^login/send/sms/', account.login_send_sms, name='login_send_sms'),
]