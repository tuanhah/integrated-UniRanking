from django.forms import ValidationError

from criterion.models import Criterion
from score.forms import ScoreForm
from subject.models import SubjectScoreByCriterion

class SubjectScoreByCriterionForm(ScoreForm):
    class Meta:
        model = SubjectScoreByCriterion
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'criterion' in self.fields:
            self.fields['criterion'].queryset = self.model.get_editable_criterion_queryset()

class SubjectScoreByCriterionCreateForm(SubjectScoreByCriterionForm):
    pass

class SubjectScoreByCriterionEditForm(SubjectScoreByCriterionForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This university's subject does not have this criterion score"
        },
    }
    
    def clean(self):
        cleaned_data = super().clean()
        if 'univ_subject' not in self.errors and 'criterion' not in self.errors:
            univ_subject = cleaned_data['univ_subject']
            criterion = cleaned_data['criterion']
            try:
                subject_score_by_criterion = univ_subject.criterion_scores.get(criterion = criterion)
            except SubjectScoreByCriterion.DoesNotExist:
                raise ValidationError(
                    self.error_messages['__all__']['does_not_exist'], 
                    code="invalid",
                )
            else:
                self.instance = subject_score_by_criterion
        return cleaned_data

    def save(self, commit = True):
        instance = super().save(commit = False)
        instance.score = self.cleaned_data["score"]
        instance.save(update_fields=["score"])

    def delete(self):
        self.instance.delete()

