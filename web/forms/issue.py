from django import forms
from utils.Bootstrap import BootstrapForm,BootstrapModelForm
from web import models

class IssueModelForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = models.Issues
        exclude = ['project','creator','create_datetime','latest_update_datetime']
        widgets = {
            "assign":forms.Select(attrs={'class':'selectpicker',"data-live-search":"true"}),
            "attention":forms.SelectMultiple(attrs={'class':'selectpicker',"data-live-search":"true","data-actions-box":"true"}),
        }

