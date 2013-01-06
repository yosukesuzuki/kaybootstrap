from kay.utils import forms
from kay.utils.forms.modelform import ModelForm
from mainapp.models import AdminPage 

class AdminPageForm(ModelForm):
    class Meta:
         model = AdminPage 
         exclude = ('images','page_order','update','created')

