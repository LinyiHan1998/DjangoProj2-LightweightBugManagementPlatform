from django import forms

class BootstrapModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():

            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Please type in %s'%(field.label,)

class BootstrapForm(forms.Form):
    bootstrap_class_exclude = []
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'Please type in %s'%(field.label,)
