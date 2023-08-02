
from django.shortcuts import render

from web.forms.issue import IssueModelForm

def issue(request,project_id):
    form = IssueModelForm()
    return render(request,'web/issue.html',{'form':form})