import boto3
import logging
from django.shortcuts import render
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from web import models
from web.forms.file import FolderModelForm,FileModelForm
from utils.aws.awsS3 import AwsS3

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

def file_delete(request,project_id):
    aws = AwsS3()
    fid = request.GET.get('fid', '')
    delete_obj = models.Files.objects.filter(id=fid,project_id=request.tracer.project).first()
    if delete_obj.type == 2:
        # delete file in database, S3, release used space
        request.tracer.project.use_space -= delete_obj.size
        request.tracer.project.save()

        #delete file in S3
        aws.delete_file('zxcvfdgvc',request.tracer.project.key)

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

@csrf_exempt
def cos_credential(request,project_id):
    aws = AwsS3()
    data=aws.cos_credential()
    print(data)
    return JsonResponse({'status':True,'data':data})

@csrf_exempt
def file_post(request,project_id):
    print('entering file post')
    print(request.POST)
    pass


def file_download(request,project_id,file_id):
    pass