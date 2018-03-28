from django import forms
from django.core.exceptions import ValidationError

from criteria.models import Criterion
from criteria.forms import ScoreForm
from university.models import UniversitySubject
from .models import Subject, SubjectScore, SubjectScoreByCategory


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectScoreForm(ScoreForm):
    univ_subject = forms.ModelChoiceField(queryset = None)

    class Meta: 
        model = SubjectScore
        exclude = ['score_by_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = Criterion.objects.filter(category__university_only = False)
        self.fields['univ_subject'].queryset = UniversitySubject.objects.all()
        if self.instance.pk is not None: #for editing object
            self.fields['univ_subject'].initial = self.instance.score_by_category.univ_subject
            self.fields['univ_subject'].disabled = True
            self.fields['criterion'].disabled = True
            
    def get_criterion_scores_of_category(self, category):
        all_criteria = self.fields['criterion'].queryset.filter(category = category)
        added_criteria = []
        try:
            score_by_category = self.cleaned_data['univ_subject'].scores_by_category.get(criterion_category = category)
        except SubjectScoreByCategory.DoesNotExist:
            pass
        else:
            for subj_score in score_by_category.cri_scores.select_related('criterion'):
                criterion = subj_score.criterion
                score = subj_score.score
                added_criteria.append({"id": criterion.id, "name" : criterion.name, 'description' : criterion.description, "score" : score})
        non_added_criteria_queryset = all_criteria.exclude(pk__in = [criterion["id"] for criterion in added_criteria])
        non_added_criteria = [{"id" : criterion.id, "name" : criterion.name, 'description' : criterion.description} for criterion in non_added_criteria_queryset.all()]
        return (added_criteria, non_added_criteria)

class SubjectScoreAddForm(SubjectScoreForm):
    def clean(self):
        cleaned_data = super().clean()
        if "criterion" not in self.errors and "univ_subject" not in self.errors:
            univ_subject = cleaned_data['univ_subject']
            criterion = cleaned_data['criterion']
            criterion_category = criterion.category
            subject_score_by_category, created = univ_subject.scores_by_category.get_or_create(criterion_category = criterion_category)
            subject_score =  self.instance
            subject_score.score_by_category = subject_score_by_category
        return cleaned_data

    def validate_unique(self):
        # override for ignoring default argument (exclude list) which contains score_by_category, need for unique_together validate when create new object
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e)


class AddedSubjectScoreForm(SubjectScoreForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This university's subject does not have this criterion score"
        },
    }

    def clean(self):
        if "criterion" not in self.errors:
            univ_subject = self.cleaned_data['univ_subject']
            criterion = self.cleaned_data['criterion']
            criterion_category = criterion.category_id
            try:
                subject_score_by_category = univ_subject.scores_by_category.get(criterion_category = criterion_category)
                subject_score = subject_score_by_category.cri_scores.get(criterion = criterion)
            except (SubjectScoreByCategory.DoesNotExist, SubjectScore.DoesNotExist):
                raise forms.ValidationError(
                    self.error_messages['__all__']['does_not_exist'], 
                    code="invalid",
                )
            else:
                self.subject_score = subject_score
        return self.cleaned_data

    def get_subject_score_object(self):
        return self.subject_score

class SubjectScoreEditForm(AddedSubjectScoreForm):
    def save(self, commit = True):
        subject_score = self.subject_score
        subject_score.score = self.cleaned_data['score']
        subject_score.save(update_fields = ['score'])
        return subject_score

class SubjectScoreDeleteForm(AddedSubjectScoreForm):
    def delete_object(self):
        self.subject_score.delete()
