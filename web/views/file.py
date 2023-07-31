
from django.shortcuts import render
from django.forms import model_to_dict

from web import models
from web.forms.file import FolderModelForm,FileModelForm

def file(request,project_id):
    parent_obj = None
    folder_id=request.GET.get('folder',"")
    if folder_id.isdecimal():
        parent_obj = models.Files.objects.filter(id=int(folder_id),type=2,project_id=request.tracer.project).first()
    if request.method == 'GET':
        breadcrumb_list=[]
        parent=parent_obj
        while parent:
            breadcrumb_list.insert(0,model_to_dict(parent,['id','name']))
            parent = parent.parent
        queryset = models.Files.objects.filter(project_id=request.tracer.project)
        if parent_obj:
            file_object_list = queryset.filter(parent=parent_obj).order_by('type')
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
        return render(request,'web/file.html',context)



    return render(request,'web/file.html')

def file_delete(request,project_id):
    pass


def cos_credential(request,project_id):
    pass

def file_post(request,project_id):
    pass

def file_download(request,project_id,file_id):
    pass