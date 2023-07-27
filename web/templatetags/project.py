from django.template import Library
from web import models

register = Library()

@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    #1.获取创建所有项目
    create_proj_list = models.Project.objects.filter(creator=request.tracer.user)
    #2.获取参与的所有项目
    join_proj_list = models.ProjectUser.objects.filter(userId=request.tracer.user)
    return {'my':create_proj_list,'join':join_proj_list}