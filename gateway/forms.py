from django import forms
from gateway.models import InfoModel

class InfoForm(forms.ModelForm):
    class Meta:
        model=InfoModel
        fields='__all__'
