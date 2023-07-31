from django.shortcuts import render
def dashboard(request,project_id):
    return render(request,'web/dashboard.html')

def issue(request,project_id):
    return render(request,'web/issue.html')

def statistics(request,project_id):
    return render(request,'web/statistics.html')


def setting(request,project_id):
    return render(request,'web/setting.html')