from Analysis.models import Details
from django.forms import ModelForm

class DetailForm(ModelForm):

    class Meta:
        model = Details
        fields = ['document','name']