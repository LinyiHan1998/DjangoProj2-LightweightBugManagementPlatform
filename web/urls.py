# from django.conf.urls import url,include
# from web.views import account, home, project, statistics, wiki, file, setting, issue,dashboard
#
# urlpatterns = [
#     url(r'^register/', account.register, name='register'),
#     url(r'^login/sms/', account.login_sms, name='login_sms'),
#     url(r'^login/username', account.login, name='login'),
#     url(r'^image/code', account.image_code, name='image_code'),
#     url(r'^send/sms/', account.send_sms, name='send_sms'),
#     url(r'^login/send/sms/', account.login_send_sms, name='login_send_sms'),
#     url(r'^index/', home.index, name='index'),
#     url(r'^logout/', account.logout, name='logout'),
#
#     url(r'^price/', home.price, name='price'),
#     url(r'^payment/(?P<policy_id>\d+)/', home.payment, name='payment'),
#     url(r'^pay/$', home.pay, name='pay'),
#     url(r'^pay/execute/$', home.execute, name='execute'),
#
#     #Managing Projects
#     url(r'^project/list', project.project_list, name='project_list'),
#     url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
#     url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
#
#
#     #project detail page
#     url('^manage/(?P<project_id>\d+)/',include([
#         url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
#         url(r'^dashboard/issues/count$', dashboard.issues_count, name='issues_count'),
#
#
#         url(r'^statistics/$', statistics.statistics, name='statistics'),
#         url(r'^statistics/priority$', statistics.statistics_priority, name='statistics_priority'),
#         url(r'^statistics/project/user$', statistics.statistics_project_user, name='statistics_project_user'),
#
#         #issue
#         url(r'^issue/$', issue.issue, name='issue'),
#         url(r'^issue/detail/(?P<issues_id>\d+)/$', issue.issues_detail, name='issues_detail'),
#         url(r'^issue/record/(?P<issues_id>\d+)/$', issue.issues_record, name='issues_record'),
#         url(r'^issue/change/(?P<issues_id>\d+)/$', issue.issues_change, name='issues_change'),
#         url(r'^issue/invite/url/$', issue.invite_url, name='invite_url'),
#
#
#
#         #files
#         url(r'^file/$', file.file, name='file'),
#         url(r'^file/delete/$', file.file_delete, name='file_delete'),
#         url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),
#         url(r'^file/post/$', file.file_post, name='file_post'),
#         url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),
#
#
#         #wiki
#         url(r'^wiki/$', wiki.wiki, name='wiki'),
#         url(r'^wiki/add$', wiki.wiki_add, name='wiki_add'),
#         url(r'^wiki/catalog$', wiki.wiki_catalog, name='wiki_catalog'),
#         url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
#         url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
#         url(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),
#
#
#         #settings
#         url(r'^setting/$', setting.setting, name='setting'),
#         url(r'^setting/delete/$', setting.setting_delete, name='setting_delete'),
#
#     ], None, None)),
#         url(r'^invite/join/(?P<code>\w+)/$', issue.invite_join, name='invite_join'),
# ]
from django.conf.urls import url,include
from web.views import account, home, project, statistics, wiki, file, setting, issue,dashboard
from rest_framework.routers import DefaultRouter
from web.views import account, home, project, statistics, wiki, file, setting, issue, dashboard
from web.views.serialize import (UserInfoViewSet, PriceStrategyViewSet, TransactionViewSet, ProjectViewSet,
                       ProjectUserViewSet, WikiViewSet, FilesViewSet, ModuleViewSet, IssueTypeViewSet,
                       IssuesViewSet, IssuesReplyViewSet, ProjectInviteViewSet)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your API",
#         default_version='v1',
#         description="Your API description",
#         terms_of_service="https://www.yourapp.com/terms/",
#         contact=openapi.Contact(email="contact@yourapp.com"),
#         license=openapi.License(name="Your License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )
router = DefaultRouter()
router.register(r'users', UserInfoViewSet)
router.register(r'price-strategies', PriceStrategyViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-users', ProjectUserViewSet)
router.register(r'wikis', WikiViewSet)
router.register(r'files', FilesViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'issue-types', IssueTypeViewSet)
router.register(r'issues', IssuesViewSet)
router.register(r'issue-replies', IssuesReplyViewSet)
router.register(r'project-invites', ProjectInviteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),  # Include DRF router urls first
    url(r'^register/', account.register, name='register'),
    url(r'^login/sms/', account.login_sms, name='login_sms'),
    url(r'^login/username', account.login, name='login'),
    url(r'^image/code', account.image_code, name='image_code'),
    url(r'^send/sms/', account.send_sms, name='send_sms'),
    url(r'^login/send/sms/', account.login_send_sms, name='login_send_sms'),
    url(r'^index/', home.index, name='index'),
    url(r'^logout/', account.logout, name='logout'),

    url(r'^price/', home.price, name='price'),
    url(r'^payment/(?P<policy_id>\d+)/', home.payment, name='payment'),
    url(r'^pay/$', home.pay, name='pay'),
    url(r'^pay/execute/$', home.execute, name='execute'),

    #Managing Projects
    url(r'^project/list', project.project_list, name='project_list'),
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),


    #project detail page
    url('^manage/(?P<project_id>\d+)/',include([
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^dashboard/issues/count$', dashboard.issues_count, name='issues_count'),


        url(r'^statistics/$', statistics.statistics, name='statistics'),
        url(r'^statistics/priority$', statistics.statistics_priority, name='statistics_priority'),
        url(r'^statistics/project/user$', statistics.statistics_project_user, name='statistics_project_user'),

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