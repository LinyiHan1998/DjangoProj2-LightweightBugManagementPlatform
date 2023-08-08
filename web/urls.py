from django.conf.urls import url,include
from web.views import account, home, project, manage, wiki, file, setting, issue

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
        url(r'^statistics/$', manage.statistics, name='statistics'),

        #issue
        url(r'^issue/$', issue.issue, name='issue'),
        url(r'^issue/detail/(?P<issues_id>\d+)/$', issue.issues_detail, name='issues_detail'),
        url(r'^issue/record/(?P<issues_id>\d+)/$', issue.issues_record, name='issues_record'),
        url(r'^issue/change/(?P<issues_id>\d+)/$', issue.issues_change, name='issues_change'),
        url(r'^issue/invite/url/$', issue.invite_url, name='invite_url'),



        #files
        url(r'^file/$', file.file, name='file'),
        url(r'^file/delete/$', file.file_delete, name='file_delete'),
        url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),
        url(r'^file/post/$', file.file_post, name='file_post'),
        url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),


        #wiki
        url(r'^wiki/$', wiki.wiki, name='wiki'),
        url(r'^wiki/add$', wiki.wiki_add, name='wiki_add'),
        url(r'^wiki/catalog$', wiki.wiki_catalog, name='wiki_catalog'),
        url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
        url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
        url(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),


        #settings
        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^setting/delete/$', setting.setting_delete, name='setting_delete'),

    ], None, None)),
        url(r'^invite/join/(?P<code>\w+)/$', issue.invite_join, name='invite_join'),
]