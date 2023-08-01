import boto3
import logging
from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse

from web import models
from web.forms.file import FolderModelForm,FileModelForm

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
    fid = request.GET.get('fid', '')
    delete_obj = models.Files.objects.filter(id=fid,project_id=request.tracer.project).first()
    if delete_obj.type == 2:
        #delete files in database, cos, release used space
        total_size = 0
        folder_list = [delete_obj,]
        key_list = []
        for folder in folder_list:
            child_list = models.Files.objects.filter(project_id=request.tracer.project,parent=folder).order_by('type')
            for child in child_list:
                if child.type == 1:
                    folder.append(child)
                else:
                    #file
                    total_size += child.file_size
                    ket_list.append(child.key)
                    #delete in cos
                    #todo
        request.tracer.project.use_space -= delete_obj.size
        request.tracer.project.save()
    else:
        pass
    delete_obj.delete()
    return JsonResponse({'status':True})


def cos_credential(request,project_id):
    client = boto3.client('sts')
    response = client.get_session_token(DurationSeconds=3600)
    logging.info('Credentials {}'.format(response['Credentials']))
    logging.info('Leaving cos_credentisl')
    data={
        'startTime':0,
        'expiredTime':0,
        'credentials':response['Credentials']
    }
    return JsonResponse({'credentials':response['Credentials']})

def file_post(request,project_id):
    pass


def file_download(request,project_id,file_id):
    pass