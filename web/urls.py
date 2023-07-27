from django.conf.urls import url,include
from web.views import account, home, project, manage

urlpatterns = [
    url(r'^register/', account.register, name='register'),
    url(r'^login/sms/', account.login_sms, name='login_sms'),
    url(r'^login/username', account.login, name='login'),
    url(r'^image/code', account.image_code, name='image_code'),
    url(r'^send/sms/', account.send_sms, name='send_sms'),
    url(r'^login/send/sms/', account.login_send_sms, name='login_send_sms'),
    url(r'^index/', home.index, name='index'),
    url(r'^logout/', account.logout, name='logout'),

    #Managing Projects
    url(r'^project/list', project.project_list, name='project_list'),
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),


    #project detail page
    url('^manage/(?P<project_id>\d+)/',include([
        url(r'^dashboard/$', manage.dashboard, name='dashboard'),
        url(r'^issue/$', manage.issue, name='issue'),
        url(r'^statistics/$', manage.statistics, name='statistics'),
        url(r'^file/$', manage.file, name='file'),
        url(r'^wiki/$', manage.wiki, name='wiki'),
        url(r'^setting/$', manage.setting, name='setting')
    ], None, None)),

]