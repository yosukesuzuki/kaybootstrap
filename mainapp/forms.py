from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from mainapp.models import AdminTopPage 

class AdminTopPageForm(ModelForm):
    class Meta:
         model = AdminTopPage 
         exclude = ('images','page_order','update','created')

