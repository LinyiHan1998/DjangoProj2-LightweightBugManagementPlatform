
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from web import models
from web.forms.issue import IssueModelForm,IssueReplyModelForm
from utils.pagination import Pagination

def issue(request,project_id):
    if request.method == 'GET':
        form = IssueModelForm(request)
        issue_obj_list = models.Issues.objects.filter(project_id=project_id)

        page = Pagination(request, issue_obj_list, '')

        context = {
            'form': form,
            "queryset": page.queryset,
            'page_string': page.html(),
        }
        return render(request,'web/issue.html',context)
    form = IssueModelForm(request,data=request.POST)
    if form.is_valid():
        form.instance.project = request.tracer.project
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status': False,'error':form.errors})

def issues_detail(request,project_id,issues_id):

    instance = models.Issues.objects.filter(id=issues_id,project_id=project_id).first()
    form = IssueModelForm(request,instance=instance)
    return render(request,'web/issues_detail.html',{'form':form,'instance':instance})

@csrf_exempt
def issues_record(request,project_id,issues_id):
    if request.method == 'GET':
        reply_list = models.IssuesReply.objects.filter(issues_id=issues_id,issues__project=request.tracer.project)
        data_list =[]
        #将reply_list从queryset格式化为Json格式
        for row in reply_list:
            data = {
                'id':row.id,
                'reply_type_text':row.get_reply_type_display(),
                'content':row.content,
                'creator':row.creator.username,
                'datetime':row.create_datetime.strftime("%b. %-d, %Y, %-I:%-M%p"),
                'parent_id':row.reply_id
            }
            data_list.append(data)
        return JsonResponse({'status': True,'data':data_list})
    #用户提交了两个数据 content 和 reply
    form = IssueReplyModelForm(data=request.POST)
    if form.is_valid():
        form.instance.issues_id = issues_id
        form.instance.reply_type=2
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
        return JsonResponse({'status':True,'data':info})
    return JsonResponse({'status': False, 'error': form.errors})

@csrf_exempt
def issues_change(request,project_id,issues_id):
    issue_obj = models.Issues.objects.filter(id=issues_id,project_id=project_id).first()
    post_dict = json.loads(request.body.decode('utf-8'))
    #{name: "issues_type", value: "2"}
    name = post_dict.get('name')
    value = post_dict.get('value')
    print(post_dict)
    field_obj = models.Issues._meta.get_field(name)
    #1. 数据库更新
    #1.1文本字段更新
    if name in ["subject","desc","start_date","end_date"]:
        if not value:
            if not field_obj.null:
                return JsonResponse({'status':False,'error':'This field cannot be blank'})
            setattr(issue_obj, name, None)
            issue_obj.save()
            #record: xx changed to be yy
            msg = '{} changed to None'.format(field_obj.verbose_name)
            print(msg)
        else:
            setattr(issue_obj,name,value)
            issue_obj.save()
            msg = '{} changed to {}'.format(field_obj.verbose_name,value)
            print(msg)
        new_obj = models.IssuesReply.objects.create(
            reply_type=1,
            issues=issue_obj,
            content=msg,
            creator=request.tracer.user,
        )
        new_reply_dict = {
            'id': new_obj.id,
            'reply_type_text': new_obj.get_reply_type_display(),
            'content': new_obj.content,
            'creator': new_obj.creator.username,
            'datetime': new_obj.create_datetime.strftime("%b. %-d, %Y, %-I:%-M%p"),
            'parent_id': new_obj.reply_id
        }
        print(new_reply_dict)
        return JsonResponse({'status':True,'data':new_reply_dict})
    #1.2外键字段更新
    #1.3choices字段更新
    #1.4many to many字段
    #2. 生成操作记录
    return JsonResponse({})