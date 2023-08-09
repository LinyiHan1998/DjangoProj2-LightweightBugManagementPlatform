
from django.shortcuts import render

def dashboard(request,project_id):
    return render(request,'web/dashboard.html')