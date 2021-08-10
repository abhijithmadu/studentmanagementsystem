from django import forms
from .models import Assignment

class AssignementForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields =['answer']
