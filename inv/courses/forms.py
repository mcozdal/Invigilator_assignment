from django import forms
from django.forms import ModelForm
from django import forms
#from .models import 

class schedule(forms.Form):
    # name = forms.CharField(min_length=3)
    # id = forms.DecimalField()
    excel = forms.FileField()

    # number1 = forms.DecimalField()
    # number2 = forms.DecimalField()

