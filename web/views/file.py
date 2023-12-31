import json
import boto3
import logging
import requests

from django.shortcuts import render,HttpResponse
from django.forms import model_to_dict
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from web import models
from web.forms.file import FolderModelForm,FileModelForm
from utils.aws.awsS3 import AwsS3
from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def file(request,project_id):
    print('Entering file')
    parent_obj = None
    folder_id=request.GET.get('folder',"")
    print(folder_id)
    if folder_id.isdecimal():
        parent_obj = models.Files.objects.filter(id=int(folder_id),type=1,project_id=request.tracer.project).first()
        print(parent_obj)
    if request.method == 'GET':
        print('Get request')
        breadcrumb_list=[]
        parent=parent_obj
        while parent:
            breadcrumb_list.insert(0,model_to_dict(parent,['id','FileName']))
            parent = parent.parent
        queryset = models.Files.objects.filter(project_id=request.tracer.project)
        if parent_obj:
            file_object_list = queryset.filter(parent=folder_id).order_by('type')
        else:
            file_object_list = queryset.filter(parent__isnull=True).order_by('type')

        print(file_object_list)

        form = FolderModelForm(request,parent_obj)
        context = {
            'form':form,
            'file_object_list':file_object_list,
            'breadcrumb_list':breadcrumb_list,
            'folder_object':parent_obj
        }

        print(context['breadcrumb_list'])

        print('Leaving file')
        return render(request,'web/file.html',context)
    print('POST request')
    fid = request.POST.get('fid','')
    edit_obj = None
    if fid.isdecimal():
        edit_obj = models.Files.objects.filter(id=int(fid),type=1,project_id=request.tracer.project).first()
        print('Edit-obj')
        print(edit_obj)
    if edit_obj:
        form = FolderModelForm(request, parent_obj, data=request.POST,instance=edit_obj)
    else:
        form = FolderModelForm(request, parent_obj, data=request.POST)
    if form.is_valid():
        print('Form is valid')
        form.instance.project_id = request.tracer.project
        form.instance.type = 1
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_obj
        form.save()
        print('Leaving file')
        return JsonResponse({'status':True})
    print(form.errors)
    print('Leaving file')
    return JsonResponse({'status':False,'error':form.errors})

@swagger_auto_schema(method='GET', operation_description="Deleting file")
@api_view([ 'GET'])
@permission_classes([AllowAny])
def file_delete(request,project_id):
    aws = AwsS3()
    fid = request.GET.get('fid', '')
    delete_obj = models.Files.objects.filter(id=fid,project_id=request.tracer.project).first()
    if delete_obj.type == 2:
        # delete file in database, S3, release used space
        print('delete file')
        request.tracer.project.use_space -= delete_obj.size
        request.tracer.project.save()

        #delete file in S3
        aws.delete_file('zxcvfdgvc',delete_obj.key)

        #delete file in DB
        delete_obj.delete()
        return JsonResponse({'status': True})

    total_size = 0
    folder_list = [delete_obj,]
    key_list = []
    for folder in folder_list:
        child_list = models.Files.objects.filter(project_id=request.tracer.project,parent=folder).order_by('type')
        for child in child_list:
            if child.type == 1:
                folder_list.append(child)
            else:
                #file
                total_size += child.file_size

                #delete in cos
                key_list.append(child.key)
    if key_list:
        aws.delete_files('zxcvfdgvc',key_list)

    if total_size:
        request.tracer.project.use_space -= total_size
        request.tracer.project.save()

    delete_obj.delete()
    return JsonResponse({'status':True})

@swagger_auto_schema(method='POST', operation_description="Obtianing temprary cos credential")
@api_view([ 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def cos_credential(request,project_id):
    print(request.POST)
    checkFileList = json.loads(request.body.decode('utf-8'))
    per_file_limit = request.tracer.price_strategy.per_file_size * 1024 * 1024
    total_limit = request.tracer.price_strategy.project_space * 1024 * 1024 * 1024 - request.tracer.project.use_space
    tmptotal = 0
    for item in checkFileList:
        #拿到文件字节大小，单位B
        if item['size']>per_file_limit:
            return JsonResponse({'status':False,'error':"File:{} exceeds size limit (limit{}M), please upgrade your VIP".format(item['name'],request.tracer.price_strategy.per_file_size)})
        tmptotal += item['size']
        if tmptotal > total_limit:
            return JsonResponse({'status':False,'error':'Files exceed max size, please upgrade your VIP'})
    print(checkFileList)

    aws = AwsS3()
    data=aws.cos_credential()
    print(data)
    return JsonResponse({'status':True,'data':data})


@swagger_auto_schema(method='POST')
@api_view([ 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def file_post(request,project_id):
    print('entering file post')
    print(request.POST)
    form = FileModelForm(request,data=request.POST)
    print('form built')

    if form.is_valid():
        print(form)
        data_dict = form.cleaned_data
        data_dict.update({'project_id': request.tracer.project, 'type': 2, 'update_user': request.tracer.user})
        print(data_dict)
        instance = models.Files.objects.create(**data_dict)

        # 项目的已使用空间：更新 (data_dict['file_size'])
        request.tracer.project.use_space += data_dict['size']
        request.tracer.project.save()

        result = {
            'id': instance.id,
            'name': instance.FileName,
            'size': instance.size,
            'username': instance.update_user.username,
            'datetime': instance.update_datetime.strftime("%b. %-d, %Y, %-I:%-M%p"),
            'download_url': reverse('file_download', kwargs={"project_id": project_id, 'file_id': instance.id})
            # 'file_type': instance.get_file_type_display()
        }
        return JsonResponse({'status': True, 'data': result})

    return JsonResponse({'status': False, 'data': "File Error"})

@swagger_auto_schema(method='GET')
@api_view([ 'GET'])
@permission_classes([AllowAny])
def file_download(request,project_id,file_id):
    file_obj = models.Files.objects.filter(id=file_id,project_id=request.tracer.project).first()
    res = requests.get(file_obj.path)

    # 文件分块处理（适用于大文件）
    data = res.iter_content()

    # 设置content_type=application/octet-stream 用于提示下载框
    response = HttpResponse(data, content_type="application/octet-stream")
    from django.utils.encoding import escape_uri_path

    # 设置响应头：中文件文件名转义
    response['Content-Disposition'] = "attachment; filename={};".format(escape_uri_path(file_obj.FileName))
    return response