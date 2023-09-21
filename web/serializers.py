from rest_framework import serializers
from .models import (UserInfo, PriceStrategy, Transaction, Project,
                     ProjectUser, Wiki, Files, Module, IssueType, Issues,
                     IssuesReply, ProjectInvite)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

class PriceStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceStrategy
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = '__all__'

class WikiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki
        fields = '__all__'

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueType
        fields = '__all__'

class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'

class IssuesReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuesReply
        fields = '__all__'

class ProjectInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInvite
        fields = '__all__'
