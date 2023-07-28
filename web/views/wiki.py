from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from web.forms.wiki import WikiModelForm
from web import models

def wiki(request,project_id):
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request,'web/wiki.html')
    wiki_obj = models.Wiki.objects.filter(id=wiki_id,project_id=project_id).first()
    return render(request,'web/wiki.html',{'wiki_obj':wiki_obj})

def wiki_add(request,project_id):
    if request.method =='GET':
        form = WikiModelForm(request)
        return render(request,'web/wiki_add.html',{'form':form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        #判断用户是否选择了父文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('wiki',kwargs={'project_id':project_id})
        return redirect(url)

def wiki_catalog(request,project_id):
    print(1)
    data = models.Wiki.objects.filter(project_id=project_id).values("id","title","parent_id").order_by('depth','id')
    print(data)
    return JsonResponse({'status':True,'data':list(data)})
