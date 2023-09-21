from rest_framework import viewsets
from web.models import (UserInfo, PriceStrategy, Transaction, Project, ProjectUser,
                     Wiki, Files, Module, IssueType, Issues, IssuesReply, ProjectInvite)
from web.serializers import (UserInfoSerializer, PriceStrategySerializer, TransactionSerializer,
                          ProjectSerializer, ProjectUserSerializer, WikiSerializer, FilesSerializer,
                          ModuleSerializer, IssueTypeSerializer, IssuesSerializer, IssuesReplySerializer,
                          ProjectInviteSerializer)

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class PriceStrategyViewSet(viewsets.ModelViewSet):
    queryset = PriceStrategy.objects.all()
    serializer_class = PriceStrategySerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer

class WikiViewSet(viewsets.ModelViewSet):
    queryset = Wiki.objects.all()
    serializer_class = WikiSerializer

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class IssueTypeViewSet(viewsets.ModelViewSet):
    queryset = IssueType.objects.all()
    serializer_class = IssueTypeSerializer

class IssuesViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer

class IssuesReplyViewSet(viewsets.ModelViewSet):
    queryset = IssuesReply.objects.all()
    serializer_class = IssuesReplySerializer

class ProjectInviteViewSet(viewsets.ModelViewSet):
    queryset = ProjectInvite.objects.all()
    serializer_class = ProjectInviteSerializer
