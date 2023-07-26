from django import forms
from django.core.exceptions import ValidationError
from utils.Bootstrap import BootstrapForm,BootstrapModelForm
from web import models

class ProjectModelForm(BootstrapModelForm,forms.ModelForm):
    #description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = models.Project
        fields = ['name','color','description']
        widgets = {
            'description' :forms.Textarea,
            'color':forms.RadioSelect,
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request
    def clean_name(self):
        name = self.cleaned_data.get('name')
        print(self.request.tracer.user)
        user = self.request.tracer.user
        #1.当前用户是否已经创建过此项目
        exists = models.Project.objects.filter(name=name,creator=user).exists()
        if exists:
            raise ValidationError('Project Already Exist, please rename')

        #2.当前用户是否还有额度
        print(self.request.tracer.price_strategy.project_num)
        total_num = self.request.tracer.price_strategy.project_num
        used = models.Project.objects.filter(creator=user).count()
        if used >=total_num:
            raise ValidationError('Project Number reached limit, please purchase VIP')
        return name
