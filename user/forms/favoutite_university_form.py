from django import forms
from university.models import UserFavouriteUniversity

class AddFavouriteUniversityForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteUniversity
        # fields = ('user', 'university',)
        fields = ()

class RemoveFavouriteUniversityForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteUniversity
        fields = ()