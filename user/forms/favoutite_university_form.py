from django import forms
from university.models import UserFavouriteUniversity

class AddFavouriteUniversity(forms.ModelForm):
    class Meta:
        model = UserFavouriteUniversity
        field = ('user', 'university',)

class RemoveFavouriteUniversity(forms.ModelForm):
    class Meta:
        model = UserFavouriteUniversity
        field = ()