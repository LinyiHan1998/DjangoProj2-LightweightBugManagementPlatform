from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from web import models


def statistics(request,project_id):
    return render(request,'web/statistics.html')

def statistics_priority(request,project_id):
    start = request.GET.get('start')
    end = request.GET.get('end')
    data_dict = {}
    for key,text in models.Issues.priority_choices:
        data_dict[key]={'name':text,'y':0}
    #查询所有分组得到的数据量
    result = models.Issues.objects.filter(project_id=project_id,create_datetime__gte=start,create_datetime__lt=end).values('priority').annotate(ct=Count('id'))
    for item in result:
        data_dict[item['priority']]['y'] = item['ct']
    return JsonResponse({'status':True,'data':list(data_dict.values())})


def statistics_project_user(request,project_id):
    start = request.GET.get('start')
    end = request.GET.get('end')
    #1.找到所有的issue并且根据需要指派的用户分组
    all_user_dict = {
        request.tracer.project.creator.id: {
            'name': request.tracer.project.creator.username,
            'status': {item[0]: 0 for item in models.Issues.status_choices}
        },
        None: {
            'name': 'Not Assigned',
            'status': {item[0]: 0 for item in models.Issues.status_choices}
        },

    }

    user_list = models.ProjectUser.objects.filter(project_id=project_id)
    for item in user_list:
        all_user_dict[item.userId_id]={
            'name':item.userId.username,
            'status':{item[0]: 0 for item in models.Issues.status_choices}
        }

    #2. 数据库获取相关的所有问题
    issues = models.Issues.objects.filter(project_id=project_id,create_datetime__lt=end,create_datetime__gte=start)
    for issue in issues:
        if not issue.assign:
            all_user_dict[None]['status'][issue.status] += 1
        else:
            all_user_dict[issue.assign_id]['status'][issue.status] += 1

    #3.获取所有的成员
    categories = [data['name'] for data in all_user_dict.values()]
    #4
    data_result_dict = {}
    for item in models.Issues.status_choices:
        data_result_dict[item[0]] = {'name':item[1],"data":[]}

    for key,text in models.Issues.status_choices:
        for row in all_user_dict.values():
            data_result_dict[key]['data'].append(row['status'][key])
    context = {
        'status':True,
        'data':{
            'categories':categories,
            'series': list(data_result_dict.values())
        }
    }
    return JsonResponse(context)
