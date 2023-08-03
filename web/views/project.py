import time
from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings
from django.http import JsonResponse
from web.forms.project import ProjectModelForm
from web import models
from utils.aws.awsS3 import AwsS3

def project_list(request):
    if request.method =='GET':
        form = ProjectModelForm(request)
        #组成页面的几类
        project_dict = {'star':[],'create':[],'joined':[]}
        # 1.当前用户创建的所有项目
        # 2.当前用户参与的所有项目
        # 3 当前用户星标的项目
        create_proj_list = models.Project.objects.filter(
            creator=request.tracer.user
        )
        for row in create_proj_list:
            if row.star:
                project_dict['star'].append({'value':row,'type':'my'})
            else:
                project_dict['create'].append(row)

        join_proj_list = models.ProjectUser.objects.filter(
            userId=request.tracer.user
        )
        for row in join_proj_list:
            if row.star:
                project_dict['star'].append({'value':row.project,'type':'join'})
            else:
                project_dict['joined'].append(row.project)

        return render(request,'web/project_list.html',{'form':form,'project_dict':project_dict})
    form = ProjectModelForm(request,data=request.POST)
    if form.is_valid():
        #验证通过
        form.instance.creator = request.tracer.user
        project_name = form.instance.name.lower()
        #1. 为项目创建一个桶
        bucket = "zxcvfdgvc"
        #s3 = AwsS3()
        #s3.my_create_bucket(bucket)

        #把桶和区域写入数据库
        form.instance.bucket = bucket
        form.instance.region = settings.REGION_NAME
        #2. 创建项目
        instance = form.save()
        #3. 项目初始化问题类型
        issues_type_obj_list = []
        for item in models.IssueType.PROJECT_INIT_LIST:
            issues_type_obj_list.append(models.IssueType(project=instance,title=item))
        models.IssueType.objects.bulk_create(issues_type_obj_list)

        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'error':form.errors})

def project_star(request,project_type,project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id,creator=request.tracer.user).update(star=True)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, userId=request.tracer.user).update(star=True)
        return redirect('project_list')
    return HttpResponse('Error')

def project_unstar(request,project_type,project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, userId=request.tracer.user).update(star=False)
        return redirect('project_list')
    return HttpResponse('Error')
