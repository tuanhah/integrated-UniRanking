from django import forms

from university.models import University, UniversityProfile

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        exclude = ['avg_score', 'rank']
    
class UniversityProfileForm(forms.ModelForm):
    class Meta: 
        model = UniversityProfile
        exclude = ['university']

