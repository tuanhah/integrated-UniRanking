from django import forms
from criteria.models import Criterion
from .models import University, UniversitySubject, UniversityScore, UniversityScoreByCategory
from subject.models import Subject
from criteria.forms import ScoreForm


U_EDITABLE_CATEGORY_LIST = (
    (5,"Cơ Sở Vật Chất Và Quản Trị"),
)

university_queryset = University.objects.all()
filter_cri_queryset = Criterion.objects.filter(category__pk__in =  [category[0] for category in U_EDITABLE_CATEGORY_LIST])


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name']


class UniversitySubjectCreateForm(forms.ModelForm):
    error_messages = {
        '__all__' : {
            'existed' : "This university have already had this subject"
        },
    }

    def clean(self):
        cleaned_data = super().clean()
        if "university" not in self.errors and "subject" not in self.errors:
            university = cleaned_data.get("university")
            subject = cleaned_data.get("subject")
            univ_subject = UniversitySubject.objects.filter(university = university, subject = subject)
            if univ_subject.count() > 0:
                raise forms.ValidationError(
                    self.error_messages['__all__']['existed'], 
                    code="existed",
                )
        return cleaned_data
        
    class Meta: 
        model = UniversitySubject
        fields = "__all__"

class UniversitySubjectDeleteForm(forms.ModelForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This subject does not belong to this university"
        },
    }

    def clean(self):
        cleaned_data = super().clean()
        if "university" not in self.errors and "subject" not in self.errors:
            university = cleaned_data.get("university")
            subject = cleaned_data.get("subject")
            try:
                univ_subject = UniversitySubject.objects.get(university = university, subject = subject)
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

    class Meta: 
        model = UniversitySubject
        fields = "__all__"


class UniversityScoreForm(ScoreForm):    
    university = forms.ModelChoiceField(queryset = None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = filter_cri_queryset
        self.fields['university'].queryset = university_queryset
        if self.instance.pk is not None: #for editing object
            self.fields['university'].initial = self.instance.score_by_category.university
            inst_criterion = self.instance.criterion 
            if inst_criterion not in filter_cri_queryset:
                self.fields['criterion'].disabled = True
                self.fields['criterion'].empty_label = inst_criterion

    def get_criterion_scores_of_category(self, category):
        all_criteria = self.fields['criterion'].queryset.filter(category = category)
        try:
            score_by_category = self.cleaned_data['university'].scores_by_category.get(category_criterion = category)
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

    class Meta: 
        model = UniversityScore
        exclude = ['score_by_category']

class UniversityScoreEditForm(UniversityScoreForm):
    def save(self, commit=True):
        university = self.cleaned_data['university']
        criterion = self.cleaned_data['criterion']
        category_criterion = criterion.category

        univ_score_by_category, created = university.scores_by_category.get_or_create(category_criterion = category_criterion)
        university_score =  super().save(commit=False)
        university_score.score_by_category = univ_score_by_category
        if commit:
            university_score.save()
        return university_score

class UniversityScoreDeleteForm(UniversityScoreForm):
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
            category_criterion = criterion.category
            try:
                univ_score_by_category = university.scores_by_category.get(category_criterion = category_criterion)
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

