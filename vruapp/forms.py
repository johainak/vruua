
from django import forms

from .models import TDR

class AnalysisForm(forms.Form):
    unique_imsis = {}
    for choice in TDR.objects.all():
        if choice.imsi not in unique_imsis:
            unique_imsis[choice.imsi] = choice
            print choice
    imsi= forms.ChoiceField( choices=[('','---------------')]+[(choice.imsi, choice.imsi) for choice in unique_imsis.values()],label='IMSIs (identifier of user)',)
    userAgent=forms.ChoiceField(choices=[('','---------------')],label='User-Agent')

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)



