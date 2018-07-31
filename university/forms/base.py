from django import forms

from university.models import University, UniversityProfile, UserFavouriteUniversity, UserManagerUniversity

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        exclude = []
        # exclude = ['avg_score', 'rank']

class UniversityProfileForm(forms.ModelForm):
    class Meta: 
        model = UniversityProfile
        exclude = []
        # exclude = ['university']

class UserFavouriteUniversityForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteUniversity
        exclude = []

class UserManagerUniversityForm(forms.ModelForm):
    class Meta:
        model = UserManagerUniversity
        exclude = []