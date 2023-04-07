
from django import forms

class NewForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
