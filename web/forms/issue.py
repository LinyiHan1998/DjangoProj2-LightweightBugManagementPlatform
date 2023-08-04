from django import forms
from utils.Bootstrap import BootstrapForm, BootstrapModelForm
from web import models


class IssueModelForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project', 'creator', 'create_datetime', 'latest_update_datetime']
        widgets = {
            "assign": forms.Select(attrs={'class': 'selectpicker', "data-live-search": "true"}),
            "attention": forms.SelectMultiple(
                attrs={'class': 'selectpicker', "data-live-search": "true", "data-actions-box": "true"}),
            "parent": forms.Select(attrs={'class':'selectpicker', "data-live-search": "true"}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initialize data
        # 1. Obtian all Issuetype of current project
        self.fields['issues_type'].choices = models.IssueType.objects.filter(
            project=request.tracer.project).values_list('id', 'title')

        # 2.Obtain all module in current project
        module_list = [("", "Nothing selected"), ]
        module_obj_list = models.Module.objects.filter(project=request.tracer.project).values_list("id", "title")
        module_list.extend(module_obj_list)
        self.fields['module'].choices = module_list

        # 3. Assign and CC
        # Find all Creator and Attendee of this project
        total_user_list = [(request.tracer.project.creator_id, request.tracer.project.creator.username), ]
        project_user_list = models.ProjectUser.objects.filter(project=request.tracer.project).values_list('userId_id',
                                                                                                         'userId__username')
        total_user_list.extend(project_user_list)

        self.fields['assign'].choices = [("", "Nothing selected"), ] + total_user_list
        self.fields['attention'].choices = [("", "Nothing selected"), ] + total_user_list

        # 4.Parent Issue
        parent_list = [("", "Nothing selected"), ]
        parent_obj_list = models.Issues.objects.filter(project = request.tracer.project).values_list("id","subject")
        parent_list.extend(parent_obj_list)
        self.fields['parent'].choices =  parent_list


class IssueReplyModelForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = models.IssuesReply
        fields = ['content','reply']
