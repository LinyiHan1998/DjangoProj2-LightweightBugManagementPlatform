import uuid
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.aws.awsS3 import AwsS3
from web.forms.wiki import WikiModelForm
from web import models

from rest_framework.decorators import api_view,permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def wiki(request,project_id):
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request,'web/wiki.html')
    wiki_obj = models.Wiki.objects.filter(id=wiki_id,project_id=project_id).first()
    return render(request,'web/wiki.html',{'wiki_obj':wiki_obj})

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def wiki_add(request,project_id):
    if request.method =='GET':
        form = WikiModelForm(request)
        return render(request,'web/wiki_form.html',{'form':form})
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


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def wiki_catalog(request,project_id):
    print(1)
    data = models.Wiki.objects.filter(project_id=project_id).values("id","title","parent_id").order_by('depth','id')
    print(data)
    return JsonResponse({'status':True,'data':list(data)})

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
def wiki_delete(request,project_id,wiki_id):
    models.Wiki.objects.filter(id=wiki_id,project_id=project_id).first().delete()

    url = reverse('wiki',kwargs={'project_id':project_id})
    return redirect(url)

@swagger_auto_schema(method='get')
@swagger_auto_schema(method='POST')
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def wiki_edit(request,project_id,wiki_id):

    wiki_obj = models.Wiki.objects.filter(project_id=project_id,id=wiki_id).first()

    if not wiki_obj:
        url = reverse('wiki',kwargs={'project_id':project_id})
        return redirect(url)
    if request.method == 'GET':
        form = WikiModelForm(request,instance=wiki_obj)
        return render(request,'web/wiki_form.html',{'form':form})
    form = WikiModelForm(request,instance=wiki_obj,data=request.POST)
    if form.is_valid():
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        preview_url = "{0}?wiki_id={1}".format(url,wiki_id)
        return redirect(preview_url)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def wiki_upload(request,project_id):
    res_list = {
        'success': None,
        'message': None,
        'url': None
    }
    print(1)
    upload_data = request.FILES.get('editormd-image-file')
    if not upload_data:
        res_list['message'] = 'Image does not exist'
        return JsonResponse(res_list)
    ext = upload_data.name.rsplit('.')[-1]
    key = "{}.{}".format(uuid.uuid4(),ext)

    print(upload_data)
    print(key)

    s3_imageUpload = AwsS3()
    image_url = 'https://zxcvfdgvc.s3.us-west-1.amazonaws.com/'+key
    s3_imageUpload.upload_single_photo(upload_data, key, request.tracer.project.bucket)

    res_list['success'] = 1
    res_list['url'] = image_url
    return JsonResponse(res_list)
