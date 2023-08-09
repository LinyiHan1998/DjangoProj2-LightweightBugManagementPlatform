import json
import pytz
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

from web import models
from web.forms.issue import IssueModelForm, IssueReplyModelForm, InviteModelForm
from utils.pagination import Pagination
from utils.encrypt import uid


class CheckFilter(object):
    def __init__(self, name, data_list, request):
        self.name = name
        self.data_list = data_list
        self.request = request

    def __iter__(self):
        for data in self.data_list:
            key = str(data[0])
            text = data[1]
            ck = ''
            value_list = self.request.GET.getlist(self.name)
            if key in value_list:
                ck = 'checked'
                value_list.remove(key)
            else:
                value_list.append(key)
            # 为自己生成url
            # 在当前URL基础上增加一项
            query_dict = self.request.GET.copy()
            query_dict._mutable = True
            query_dict.setlist(self.name, value_list)  # {'status:[1,2,3]}
            if 'page' in query_dict:
                query_dict.pop('page')
            param_url = query_dict.urlencode()
            if param_url:
                url = "{}?{}".format(self.request.path_info,param_url )  # status=1&status=2&status=3
            else:
                url=self.request.path_info
            tpl = '<a class="cell" href="{url}"><input type="checkbox" {ck} /><label>{text}</label></a>'
            html = tpl.format(url=url, ck=ck, text=text)
            # print(html)
            yield mark_safe(html)
class SelectFilter(object):
    def __init__(self,name,datalist,request):
        self.name = name
        self.datalist = datalist
        self.request = request
    def __iter__(self):
        yield mark_safe("<select class='select2' multiple='multiple' style='width:100%'>")
        for data in self.datalist:
            key = str(data[0])
            text = data[1]
            selected = ""
            value_list = self.request.GET.getlist(self.name)
            if key in value_list:
                selected='selected'
                value_list.remove(key)
            else:
                value_list.append(key)
            query_dict = self.request.GET.copy()
            query_dict._mutable=True
            query_dict.setlist(self.name,value_list)
            if 'page' in query_dict:
                query_dict.pop('page')
            param_url = query_dict.urlencode()
            if param_url:
                url = '{}?{}'.format(self.request.path_info,param_url)
            else:
                url = self.request.path_info
            html = "<option value='{url}' {selected}>{text}</option>".format(url=url,selected=selected,text=text)
            yield mark_safe(html)
        yield mark_safe("</select>")
def issue(request, project_id):
    if request.method == 'GET':
        print(request.GET)
        print(request.GET.getlist('status'))

        allow_filter_name = ['issues_type', 'priority', 'status','assign','attention','mode','parent']
        condition = {}
        for name in allow_filter_name:
            value_list = request.GET.getlist(name)
            if not value_list:
                continue
            condition["{}__in".format(name)] = value_list
        form = IssueModelForm(request)
        issue_obj_list = models.Issues.objects.filter(project_id=project_id).filter(**condition)

        page = Pagination(request, issue_obj_list, '')

        project_total_user = [(request.tracer.project.creator_id,request.tracer.project.creator.username)]
        project_join_user = models.ProjectUser.objects.filter(project_id = project_id).values_list('userId_id','userId__username')
        project_total_user.extend(project_join_user)
        invite_form = InviteModelForm()
        context = {
            'form': form,
            'invite_form':invite_form,
            "queryset": page.queryset,
            'page_string': page.html(),
            'filter_list':[
                {'title': 'Status', 'filter':CheckFilter('status', models.Issues.status_choices, request)},
                {'title': 'Priority', 'filter': CheckFilter('priority', models.Issues.priority_choices, request)},
                {'title': 'Issue Type', 'filter': CheckFilter('issues_type', models.IssueType.objects.filter(project_id=project_id).values_list('id','title'), request)},
                {'title': 'Assign', 'filter': SelectFilter('assign', project_total_user, request)},
                {'title': 'Attention', 'filter': SelectFilter('attention', project_total_user, request)},
            ],
        }
        return render(request, 'web/issue.html', context)
    form = IssueModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def issues_detail(request, project_id, issues_id):
    instance = models.Issues.objects.filter(id=issues_id, project_id=project_id).first()
    form = IssueModelForm(request, instance=instance)
    return render(request, 'web/issues_detail.html', {'form': form, 'instance': instance})
@csrf_exempt
def issues_record(request, project_id, issues_id):
    if request.method == 'GET':
        reply_list = models.IssuesReply.objects.filter(issues_id=issues_id, issues__project=request.tracer.project)
        data_list = []
        # 将reply_list从queryset格式化为Json格式
        for row in reply_list:
            data = {
                'id': row.id,
                'reply_type_text': row.get_reply_type_display(),
                'content': row.content,
                'creator': row.creator.username,
                'datetime': row.create_datetime.strftime("%b. %-d, %Y, %-I:%-M%p"),
                'parent_id': row.reply_id
            }
            data_list.append(data)
        return JsonResponse({'status': True, 'data': data_list})
    # 用户提交了两个数据 content 和 reply
    form = IssueReplyModelForm(data=request.POST)
    if form.is_valid():
        form.instance.issues_id = issues_id
        form.instance.reply_type = 2
        form.instance.creator = request.tracer.user
        instance = form.save()
        info = {
            'id': instance.id,
            'reply_type_text': instance.get_reply_type_display(),
            'content': instance.content,
            'creator': instance.creator.username,
            'datetime': instance.create_datetime.strftime("%b. %-d, %Y, %-I:%-M%p"),
            'parent_id': instance.reply_id
        }
        return JsonResponse({'status': True, 'data': info})
    return JsonResponse({'status': False, 'error': form.errors})
@csrf_exempt
def issues_change(request, project_id, issues_id):
    issue_obj = models.Issues.objects.filter(id=issues_id, project_id=project_id).first()
    post_dict = json.loads(request.body.decode('utf-8'))
    # {name: "issues_type", value: "2"}
    name = post_dict.get('name')
    value = post_dict.get('value')
    print(post_dict)
    field_obj = models.Issues._meta.get_field(name)

    def create_reply_record(content):
        new_object = models.IssuesReply.objects.create(
            reply_type=1,
            issues=issue_obj,
            content=msg,
            creator=request.tracer.user,
        )
        new_reply_dict = {
            'id': new_object.id,
            'reply_type_text': new_object.get_reply_type_display(),
            'content': new_object.content,
            'creator': new_object.creator.username,
            'datetime': new_object.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': new_object.reply_id
        }
        return new_reply_dict

    # 1. 数据库更新
    # 1.1文本字段更新
    if name in ["subject", "desc", "start_date", "end_date"]:
        if not value:
            if not field_obj.null:
                return JsonResponse({'status': False, 'error': 'This field cannot be blank'})
            setattr(issue_obj, name, None)
            issue_obj.save()
            # record: xx changed to be yy
            msg = '{} changed to None'.format(field_obj.verbose_name)
            print(msg)
        else:
            setattr(issue_obj, name, value)
            issue_obj.save()
            msg = '{} changed to {}'.format(field_obj.verbose_name, value)
            print(msg)

        return JsonResponse({'status': True, 'data': create_reply_record(msg)})
    # 1.2外键字段更新
    if name in ['issues_type', 'module', 'assign', 'parent']:
        if not value:
            if not field_obj.null:
                return JsonResponse({'status': False, 'error': 'This field cannot be blank'})
            setattr(issue_obj, name, None)
            issue_obj.save()
            # record: xx changed to be yy
            msg = '{} changed to None'.format(field_obj.verbose_name)
            print(msg)
        else:
            if name == 'assign':
                # 是否是项目的参与者
                # 是否是项目的创建者
                if value == str(request.tracer.project.creator_id):
                    instance = request.tracer.project.creator
                else:
                    project_user = models.ProjectUser.objects.filter(project_id=project_id, userId=value).first()
                    if project_user:
                        instance = project_user.userId
                    else:
                        instance = None
                if not instance:
                    return JsonResponse({'status': False, 'error': "user is not in this project"})
                setattr(issue_obj, name, instance)
                issue_obj.save()
                # record: xx changed to be yy
                msg = '{} changed to {}'.format(field_obj.verbose_name, str(instance))
                print(msg)
            else:
                instance = field_obj.rel.model.objects.filter(id=value, project_id=project_id).first()
                if not instance:
                    return JsonResponse({'status': False, 'error': "Selected value doesn't exist"})
                setattr(issue_obj, name, instance)
                issue_obj.save()
                # record: xx changed to be yy
                msg = '{} changed to {}'.format(field_obj.verbose_name, str(instance))
                print(msg)

        return JsonResponse({'status': True, 'data': create_reply_record(msg)})
    # 1.3choices字段更新
    if name in ['status', 'mode', 'priority']:
        select_text = None
        for key, text in field_obj.choices:
            if str(key) == value:
                select_text = text
        if not select_text:
            return JsonResponse({'status': False, 'error': "Value doesn't exist"})
        setattr(issue_obj, name, value)
        issue_obj.save()
        # record: xx changed to be yy
        msg = '{} changed to {}'.format(field_obj.verbose_name, select_text)
        print(msg)
        return JsonResponse({'status': True, 'data': create_reply_record(msg)})
    # 1.4many to many字段
    if name == 'attention':
        if not isinstance(value, list):
            return JsonResponse({'status': False, 'error': 'Data Format Error'})
        if not value:
            issue_obj.attention.set(value)
            issue_obj.save()
            msg = '{} changed to None'.format(field_obj.verbose_name)
        else:
            # 获取当前项目的所有成员
            user_dict = {str(request.tracer.project.creator_id): request.tracer.project.creator.username}
            project_user_list = models.ProjectUser.objects.filter(project_id=project_id)
            for item in project_user_list:
                user_dict[str(item.userId)] = item.user.username
            username_list = []
            for user_id in value:
                username = user_dict.get(str(user_id))
                if not username:
                    return JsonResponse({'status': False, 'error': 'Data Error'})
                username_list.append(username)
            issue_obj.attention.set([])
            issue_obj.save()
            msg = '{} changed to {}'.format(field_obj.verbose_name, ','.join(username_list))
        return JsonResponse({'status': True, 'data': create_reply_record(msg)})

    # 2. 生成操作记录
    return JsonResponse({'status': False, 'data': 'Invalid action'})

@csrf_exempt
def invite_url(request,project_id):
    form = InviteModelForm(data=request.POST)
    if form.is_valid():
        #1.创建随机验证码
        #2.验证码保存到数据库
        #3.限制只有创建者可以邀请
        if request.tracer.user != request.tracer.project.creator:
            form.add_error('period','Only Project Creator can invite new member')
            return JsonResponse({'status':False,'error':form.errors})
        random_invite_code = uid(request.tracer.user.email)
        form.instance.project = request.tracer.project
        form.instance.code = random_invite_code
        form.instance.creator = request.tracer.user
        form.save()
        url_path = reverse('invite_join',kwargs={'code':random_invite_code})
        url = '{scheme}://{host}{path}'.format(
            scheme = request.scheme,
            host = request.get_host(),
            path=url_path)
        return JsonResponse({'status':True,'data':url})
    return JsonResponse({'status':False,'error':form.errors})


def invite_join(request,code):
    """访问邀请码"""
    current_datetime = datetime.datetime.now()
    invite_obj = models.ProjectInvite.objects.filter(code=code).first()

    if not invite_obj:
        return render(request,'web/invite_join.html',{'error':'Invite Code does not exist'})

    if invite_obj.project.creator == request.tracer.user:
        return render(request,'web/invite_join.html',{'error':'Creator does not need to join project'})

    if models.UserInfo.objects.filter(project=invite_obj.project,username=request.tracer.user).exists():
        return render(request, 'web/invite_join.html', {'error': 'Your are already in this project'})
    #允许的最多成员数量
    #根据项目的创建者所购买额度判定
    #获得交易记录后，判断交易是否已过期，若已过期则使用免费额度
    max_transaction=models.Transaction.objects.filter(userId = invite_obj.project.creator).order_by('-id').first()
    if max_transaction.price_strategy.category==1:
        max_mem = max_transaction.price_strategy.project_mem
    else:
        if current_datetime < max_transaction.validUntil:
            free_obj =  models.PriceStrategy.objects.filter(category=1).first()
            max_mem =free_obj.project_mem
        else:
            max_mem = max_transaction.price_strategy.project_mem

    # 允许的最多成员数量
    cur_mem = models.ProjectUser.objects.filter(project=invite_obj.project).count()
    cur_mem += 1
    if cur_mem >= max_mem:
        return render(request, 'web/invite_join.html', {'error': 'Member Number exceeds limit, please upgrade membership'})


    limit_datetime = invite_obj.create_datetime + datetime.timedelta(minutes=invite_obj.period)
    if current_datetime > limit_datetime:
        return render(request, 'web/invite_join.html', {'error': 'Invite Code expired'})

    if invite_obj.count:
        if invite_obj.used_count >= invite_obj.count:
            return render(request, 'web/invite_join.html',{'error':'Invite Code Chances are exhuasted'})
        invite_obj.use_count += 1
        invite_obj.save()

    models.ProjectUser.objects.create(userId=request.tracer.user, project=invite_obj.project)
    invite_obj.project.join_count += 1
    invite_obj.project.save()
    return render(request, 'web/invite_join.html', {'project': invite_obj.project})

