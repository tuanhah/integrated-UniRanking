from django import forms
from django.core.exceptions import ValidationError

from subject.models import SubjectGroup, Subject, UniversitySubject

class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        exclude = []

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = []

class UniversitySubjectForm(forms.ModelForm):
    class Meta: 
        model = UniversitySubject
        exclude = ('avg_score', 'rank')

class UniversitySubjectCreateForm(UniversitySubjectForm):
    pass

class UniversitySubjectDeleteForm(UniversitySubjectForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This subject does not belong to this university"
        },
    }
    
    def clean(self):
        # does not need to call super().clean() 
        # because this will enable validate_unique which does not play any role in our delete form
        cleaned_data = self.cleaned_data 
        university = cleaned_data.get("university")
        subject = cleaned_data.get("subject")
        try:
            univ_subject = UniversitySubject.objects.select_related("subject").get(university = university, subject = subject)
        except UniversitySubject.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['__all__']['does_not_exist'], 
                code="invalid",
            )
        else:
            self.instance = univ_subject
        return cleaned_data

    def delete(self):
        self.instance.delete()


