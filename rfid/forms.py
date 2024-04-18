from django import forms
from .models import Etudiant

class EtudiantForm(forms.ModelForm):
    
    uid = forms.CharField(
        label = 'UID de votre carte',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))
    name = forms.CharField(
        label = 'Nom',
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}), required=True)
    
    class Meta:
        model = Etudiant
        fields = ['uid', 'name', ]
       
       
   
       