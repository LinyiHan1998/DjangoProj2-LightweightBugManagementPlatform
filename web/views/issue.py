
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