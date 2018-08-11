from django import forms
from university.models import UserManagerUniversity
from subject.models import UniversitySector

class AddUniversitySectorForm(forms.ModelForm):
    class Meta:
        model = UniversitySector
        fields = ('sector',)

class RemoveUniversitySectorForm(forms.ModelForm):
    class Meta:
        model = UniversitySector
        fields = ('sector',)
