
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

def issues_detail(request,project_id):
    pass