from django import forms
from django.core.exceptions import ValidationError
from utils.Bootstrap import BootstrapForm,BootstrapModelForm
from web import models

class FolderModelForm(BootstrapModelForm,forms.ModelForm):
    class Meta:
        model = models.Files
        fields = ['FileName',]

    def __init__(self,request,parent_obj,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_obj = parent_obj

    def clean_FileName(self):
        print('clean_filename')
        FileName = self.cleaned_data.get('FileName')

        queryset = models.Files.objects.filter(FileName=FileName,type=1,project_id=self.request.tracer.project)
        print(queryset)
        if self.parent_obj:
            print(1)
            exists = queryset.filter(parent= self.parent_obj).exists()
        else:
            print(2)
            exists = queryset.filter(parent__isnull=True).exists()

        if exists:
            print(3)
            raise ValidationError('File already exists')
        return FileName

class FileModelForm(BootstrapModelForm,forms.ModelForm):
    etag = forms.CharField(label='ETag')

    class Meta:
        model = models.Files
        exclude = ['project_id','type','update_user','update_datetime']

        def __init__(self,request,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.request = request

        def clean_path(self):
            return "https://{}".format(self.cleaned_data.get('path'))