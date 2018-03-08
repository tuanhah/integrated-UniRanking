from django import forms
from criteria.models import Criterion
from university.models import UniversitySubject
from .models import SubjectScore, SubjectScoreByCategory
from university.forms import EDITABLE_CATEGORY_LIST as EXCLUDE_CATEGORY_LIST

univ_subj_queryset = UniversitySubject.objects.all()
filter_cri_queryset = Criterion.objects.exclude(category__pk__in =  [category[0] for category in EXCLUDE_CATEGORY_LIST])

class SubjectScoreForm(forms.ModelForm):

    error_messages = {
        'score' : {
            'invalid_number' : "Score is greater equal than 0 or lower equal than 10"
        }
    }

    univ_subject = forms.ModelChoiceField(queryset = None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = filter_cri_queryset
        self.fields['univ_subject'].queryset = univ_subj_queryset
        if self.instance.pk is not None:
            self.fields['univ_subject'].initial = self.instance.score_by_category.univ_subject.pk

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 10:
            raise forms.ValidationError(
                self.error_messages['score']['invalid_number']
            )
        return score

    def save(self, commit=True):
        univ_subject = self.cleaned_data['univ_subject']
        criterion = self.cleaned_data['criterion']
        subject_score =  super().save(commit=False)
        try:
            existed_subject_score = SubjectScore.objects.filter(score_by_category__in = univ_subject.scores_by_category.all()).get(criterion = criterion)
            existed_subject_score.score = self.cleaned_data['score']
            existed_subject_score.save(update_fields = ['score'])
        except SubjectScore.DoesNotExist: 
            subject_score.save(univ_subject = univ_subject)        
        return subject_score

    class Meta: 
        model = SubjectScore
        exclude = ['score_by_category']