from django import forms
from criteria.models import Criterion
from criteria.forms import ScoreForm
from university.models import UniversitySubject
from .models import Subject, SubjectScore, SubjectScoreByCategory
from university.forms import U_EDITABLE_CATEGORY_LIST as S_EXCLUDE_CATEGORY_LIST

univ_subj_queryset = UniversitySubject.objects.all()
filter_cri_queryset = Criterion.objects.exclude(category__pk__in =  [category[0] for category in S_EXCLUDE_CATEGORY_LIST])

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"

class SubjectScoreForm(ScoreForm):
    univ_subject = forms.ModelChoiceField(queryset = None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = filter_cri_queryset
        self.fields['univ_subject'].queryset = univ_subj_queryset
        if self.instance.pk is not None: #for editing object
            self.fields['univ_subject'].initial = self.instance.score_by_category.univ_subject
            
    def get_criterion_scores_of_category(self, category):
        all_criteria = self.fields['criterion'].queryset.filter(category = category)
        try:
            score_by_category = self.cleaned_data['univ_subject'].scores_by_category.get(category_criterion = category)
        except SubjectScoreByCategory.DoesNotExist:
            added_criteria = []
        else:
            added_criteria = []
            for subj_score in score_by_category.cri_scores.all():
                criterion = subj_score.criterion
                score = subj_score.score
                added_criteria.append({"id": criterion.id, "name" : criterion.name, "score" : score})
        print(added_criteria)
        non_added_criteria_queryset = all_criteria.exclude(pk__in = [criterion["id"] for criterion in added_criteria])
        non_added_criteria = [{"id" : criterion.id, "name" : criterion.name} for criterion in non_added_criteria_queryset.all()]
        return (added_criteria, non_added_criteria)

    class Meta: 
        model = SubjectScore
        exclude = ['score_by_category']

class SubjectScoreEditForm(SubjectScoreForm):
    def save(self, commit=True):
        univ_subject = self.cleaned_data['univ_subject']
        criterion = self.cleaned_data['criterion']
        category_criterion = criterion.category

        subject_score_by_category, created = univ_subject.scores_by_category.get_or_create(category_criterion = category_criterion)
        subject_score =  super().save(commit=False)
        subject_score.score_by_category = subject_score_by_category
        if commit:
            subject_score.save()
        return subject_score


class SubjectScoreDeleteForm(SubjectScoreForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This university's subject does not have this criterion score"
        },
    }

    def clean(self):
        cleaned_data = super().clean()
        if "criterion" not in self.errors:
            univ_subject = self.cleaned_data['univ_subject']
            criterion = self.cleaned_data['criterion']
            category_criterion = criterion.category
            try:
                subject_score_by_category = univ_subject.scores_by_category.get(category_criterion = category_criterion)
                subject_score = subject_score_by_category.cri_scores.get(criterion = criterion)
            except (SubjectScoreByCategory.DoesNotExist, SubjectScore.DoesNotExist):
                raise forms.ValidationError(
                    self.error_messages['__all__']['does_not_exist'], 
                    code="invalid",
                )
            else:
                self.subject_score = subject_score
        return cleaned_data

    def get_subject_score_object(self):
        return self.subject_score

