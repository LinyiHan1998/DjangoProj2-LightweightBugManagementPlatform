import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models

class TracerRequest(object):
    #将项目、用户、价格信息放到request的tracer中
    def __init__(self):
        self.user = None
        self.price_strategy = None
        self.project = None
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

        if transction_obj and transction_obj.validUntil and transction_obj.validUntil < cur_time:
            #expire
            transction_obj = models.Transaction.objects.filter(userId=user_obj, status=1,price_strategy__category=1).order_by('-id').first()

        tracer_obj.price_strategy = transction_obj.price_strategy
        request.tracer = tracer_obj

    def process_view(self,request,view,args,kwargs):
        #判断url是否以manage开头
        if not request.path_info.startswith('/manage/'):
            return
        #project_id由当前用户创建或参与
        project_id = kwargs.get('project_id')
        user = request.tracer.user
        project_obj = models.Project.objects.filter(creator=user,id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj
            return
        project_user_obj = models.ProjectUser.objects.filter(userId=user,project_id = project_id).first()
        if project_user_obj:
            request.tracer.project = project_user_obj.project
            return
        #url 以manage开头，且非当前用户创建或参与，则重定向到项目列表
        return redirect('project_list')