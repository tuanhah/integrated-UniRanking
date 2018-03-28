from django import forms
from django.core.exceptions import ValidationError

from criteria.models import Criterion
from .models import University, UniversitySubject, UniversityScore, UniversityScoreByCategory
from subject.models import Subject
from criteria.forms import ScoreForm



class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name']


class UniversitySubjectCreateForm(forms.ModelForm):
    class Meta: 
        model = UniversitySubject
        fields = "__all__"

class UniversitySubjectDeleteForm(forms.ModelForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This subject does not belong to this university"
        },
    }

    class Meta: 
        model = UniversitySubject
        fields = "__all__"

    def clean(self):
        # does not need to call super().clean() 
        # because this will enable validate_unique which does not play any roles in our delete form
        cleaned_data = self.cleaned_data 
        if "university" not in self.errors and "subject" not in self.errors:
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
                self.univ_subject = univ_subject
        return cleaned_data

    def get_univ_subject_object(self):
        return self.univ_subject


class UniversityScoreForm(ScoreForm):    
    university = forms.ModelChoiceField(queryset = None)

    class Meta: 
        model = UniversityScore
        exclude = ['score_by_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = Criterion.objects.filter(category__university_only = True)
        self.fields['university'].queryset = University.objects.all()
        if self.instance.pk is not None: #for editing object
            self.fields['university'].initial = self.instance.score_by_category.university
            self.fields['university'].disabled = True
            self.fields['criterion'].disabled = True
            inst_criterion = self.instance.criterion_id
            if not filter_cri_queryset.filter(id = inst_criterion).exists():
                self.fields['criterion'].empty_label = self.instance.criterion.name
                self.fields['score'].disabled = True

    def get_criterion_scores_of_category(self, category):
        all_criteria = self.fields['criterion'].queryset.filter(category = category)
        try:
            score_by_category = self.cleaned_data['university'].scores_by_category.get(criterion_category = category)
        except UniversityScoreByCategory.DoesNotExist:
            added_criteria = []
        else:
            added_criteria = []
            for univ_score in score_by_category.cri_scores.all():
                criterion = univ_score.criterion
                score = univ_score.score
                added_criteria.append({"id": criterion.id, "name" : criterion.name, "score" : score})
        non_added_criteria_queryset = all_criteria.exclude(pk__in = [criterion["id"] for criterion in added_criteria])
        non_added_criteria = [{"id" : criterion.id, "name" : criterion.name} for criterion in non_added_criteria_queryset.all()]
        return (added_criteria, non_added_criteria)

class UniversityScoreAddForm(UniversityScoreForm):
    def clean(self):
        cleaned_data = super().clean()
        if "criterion" not in self.errors and "university" not in self.errors:
            university = self.cleaned_data['university']
            criterion = self.cleaned_data['criterion']
            criterion_category = criterion.category

            univ_score_by_category, created = university.scores_by_category.get_or_create(criterion_category = criterion_category)
            university_score =  self.instance
            university_score.score_by_category = univ_score_by_category
        return cleaned_data

    def validate_unique(self):
        # override for ignoring default argument (exclude list) which contains score_by_category, need for unique_together validate when create new object
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)

class AddedUniversityScoreForm(UniversityScoreForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This university's subject does not have this criterion score"
        },
    }

    def clean(self):
        cleaned_data = super().clean()
        if "criterion" not in self.errors:
            university = self.cleaned_data['university']
            criterion = self.cleaned_data['criterion']
            criterion_category = criterion.category
            try:
                univ_score_by_category = university.scores_by_category.get(criterion_category = criterion_category)
                univ_score = univ_score_by_category.cri_scores.get(criterion = criterion)
            except (UniversityScoreByCategory.DoesNotExist, UniversityScore.DoesNotExist):
                raise forms.ValidationError(
                    self.error_messages['__all__']['does_not_exist'], 
                    code="invalid",
                )
            else:
                self.univ_score = univ_score
        return cleaned_data

    def get_univ_score_object(self):
        return self.univ_score

class UniversityScoreEditForm(AddedUniversityScoreForm):
    def save(self, commit = True):
        univ_score = self.univ_score
        univ_score.score = self.cleaned_data['score']
        univ_score.save(update_fields = ['score'])

class UniversityScoreDeleteForm(AddedUniversityScoreForm):
    def delete_object(self):
        self.univ_score.delete()
