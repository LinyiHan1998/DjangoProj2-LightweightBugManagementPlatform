from django.shortcuts import render
from django.http import JsonResponse
from web.forms.project import ProjectModelForm

def project_list(request):
    if request.method =='GET':
        form = ProjectModelForm(request)
        return render(request,'web/project_list.html',{'form':form})
    form = ProjectModelForm(request,data=request.POST)
    if form.is_valid():
        #验证通过
        form.instance.creator = request.tracer.user
        #创建项目
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'error':form.errors})