from django import forms
from django.core.exceptions import ValidationError

from subject.models import Sector, UniversitySector

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        exclude = []
class UniversitySectorForm(forms.ModelForm):
    class Meta:
        model = UniversitySector
        exclude = []