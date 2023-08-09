
from django.shortcuts import render
from django.db.models import Count

from web import models

def dashboard(request,project_id):
    status_dict = {}
    for key,text in models.Issues.status_choices:
        status_dict[key] = {'text':text,'count':0}
    issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    #project attendee
    user_list = models.ProjectUser.objects.filter(project_id=project_id).values_list('userId_id','userId__username')

    #最近10个问题
    top_ten = models.Issues.objects.filter(project_id=project_id,assign__isnull=False).order_by('-id')[0:10]
    context = {
        'status_dict':status_dict,
        'user_list':user_list,
        'top_ten':top_ten
    }
    return render(request,'web/dashboard.html',context)