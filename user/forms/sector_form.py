from django import forms
from subject.models import Sector

class AddSectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('name',)

class UpdateSectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('name',)

class RemoveSectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ()
