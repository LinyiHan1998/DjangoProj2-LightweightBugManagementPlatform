
from django.shortcuts import render
from django.http import JsonResponse

from web import models
from web.forms.issue import IssueModelForm
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

def issues_record(request,project_id,issues_id):
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