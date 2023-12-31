from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse

from web import models
from utils.aws.awsS3 import AwsS3

from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def setting(request,project_id):
    return render(request,'web/setting.html')

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def setting_delete(request,project_id):
    if request.method == 'GET':
        return render(request,'web/setting_delete.html')

    project_name = request.POST.get('project_name')

    if not project_name or project_name != request.tracer.project.name:
        return render(request,'web/setting_delete.html',{'error':'Invalid Project Name'})


    if request.tracer.user != request.tracer.project.creator:
        return render(request,'web/setting_delete.html',{'error':'Project can only be deleted by its creator'})

    #删除在S3桶中存储的文件+碎片
    aws = AwsS3()
    File_list = models.Files.objects.filter(project_id=request.tracer.project.id)

    for file in File_list:
        aws.delete_file(bucket_name='zxcvfdgvc',file_key=file.key)
    #删除project
    models.Project.objects.filter(id=request.tracer.project.id).delete()

    return redirect("project_list")