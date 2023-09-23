import datetime
import time

from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse

from web import models

from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request, project_id):
    status_dict = {}
    for key, text in models.Issues.status_choices:
        status_dict[key] = {'text': text, 'count': 0}
    issues_data = models.Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    # project attendee
    user_list = models.ProjectUser.objects.filter(project_id=project_id).values_list('userId_id', 'userId__username')

    # 最近10个问题
    top_ten = models.Issues.objects.filter(project_id=project_id, assign__isnull=False).order_by('-id')[0:10]
    context = {
        'status_dict': status_dict,
        'user_list': user_list,
        'top_ten': top_ten
    }
    return render(request, 'web/dashboard.html', context)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def issues_count(request, project_id):
    today = datetime.datetime.now().date()
    date_dict = {}
    for i in range(0, 30):
        date = today - datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]
    # date_dict = {
    # '2023_08-09': [1691539200000.0, 0],
    # '2023_08-08': [1691452800000.0, 0]
    # }

    result = models.Issues.objects.filter(project_id=project_id,
                                          create_datetime__gte=today - datetime.timedelta(days=30)).extra(
        select={'ctime': "strftime('%%Y-%%m-%%d',web_issues.create_datetime)"}).values('ctime').annotate(ct=Count('id'))
    #result = <QuerySet [{'ctime': '2023-08-09', 'ct': 1}]>
    data_list = [
        # [time_stamp*1000,count],
    ]
    for item in result:
        date_dict[item['ctime']][1] = item['ct']


    return JsonResponse({'status': True, 'data': list(date_dict.values())})
