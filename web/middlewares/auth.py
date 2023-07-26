import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models

class TracerRequest(object):
    def __init__(self):
        self.user = None
        self.price_strategy = None
class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):

        tracer_obj = TracerRequest()
        #若已登陆，则在request中赋值
        user_id = request.session.get('user_id',0)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        tracer_obj.user = user_obj
        request.tracer = tracer_obj

        #白名单
        if request.path_info in settings.WHITE_REGEX_LIST:
            return

        #检查用户是否登录，未登录返回登录页面
        if not request.tracer:
            return redirect('login')

        #登录成功后，访问后台惯例时，获取当前用户所拥有的额度
        #方式1: 免费额度都在交易记录中存储，获取最近的交易记录
        transction_obj = models.Transaction.objects.filter(userId=user_obj,status=1).order_by('-id').first()
        cur_time = datetime.datetime.now()

        if transction_obj.validUntil and transction_obj.validUntil < cur_time:
            #expire
            transction_obj = models.Transaction.objects.filter(userId=user_obj, status=1,price_strategy__category=1).order_by('-id').first()

        tracer_obj.price_strategy = transction_obj.price_strategy
        request.tracer = tracer_obj