from django.forms import ValidationError

from criterion.models import Criterion
from score.forms import ScoreForm
from university.models import UniversityScoreByCriterion

class UniversityScoreByCriterionForm(ScoreForm):
    class Meta:
        model = UniversityScoreByCriterion
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'criterion' in self.fields:
            self.fields['criterion'].queryset = self.model.get_editable_criterion_queryset()   

class UniversityScoreByCriterionCreateForm(UniversityScoreByCriterionForm):
    pass

class UniversityScoreByCriterionEditForm(UniversityScoreByCriterionForm):
    error_messages = {
        '__all__' : {
            'does_not_exist' : "This university does not have this criterion score"
        },
    }

    class Meta(UniversityScoreByCriterionForm.Meta): 
        exclude = UniversityScoreByCriterionForm.Meta.exclude + ['university', 'criterion']

    def clean(self):
        cleaned_data = super().clean()
        if 'university' not in self.errors and 'criterion' not in self.errors:
            university = cleaned_data['university']
            criterion = cleaned_data['criterion']
            try:
                university_score_by_criterion = university.criterion_scores.get(criterion = criterion)
            except UniversityScoreByCriterion.DoesNotExist:
                raise ValidationError(
                    self.error_messages['__all__']['does_not_exist'], 
                    code="invalid",
                )
            else:
                self.instance = university_score_by_criterion
        return cleaned_data

    def save(self, commit = True):
        instance = super().save(commit = False)
        instance.score = self.cleaned_data["score"]
        instance.save(update_fields=["score"])

    def delete(self):
        self.instance.delete()

