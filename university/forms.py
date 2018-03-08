from django import forms
from criteria.models import Criterion
from .views import University,UniversitySubject, UniversityScore


EDITABLE_CATEGORY_LIST = (
    (5,"Cơ Sở Vật Chất Và Quản Trị"),
)

university_queryset = University.objects.all()
filter_cri_queryset = Criterion.objects.filter(category__pk__in =  [category[0] for category in EDITABLE_CATEGORY_LIST])

class UniversityScoreForm(forms.ModelForm):

    error_messages = {
            'score' : {
                'invalid_number' : "Score is greater equal than 0 or lower equal than 10"
            }
        }
    
    university = forms.ModelChoiceField(queryset = None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['criterion'].queryset = filter_cri_queryset
        self.fields['university'].queryset = university_queryset
        if self.instance.pk is not None:
            self.fields['university'].initial = self.instance.score_by_category.university.pk

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 10:
            raise forms.ValidationError(
                self.error_messages['score']['invalid_number']
            )
        return score

    def save(self, commit=True):
        university = self.cleaned_data['university']
        criterion = self.cleaned_data['criterion']
        university_score =  super().save(commit=False)
        try:
            existed_uni_score = UniversityScore.objects.filter(score_by_category__in = university.scores_by_category.all()).get(criterion = criterion)
            existed_uni_score.score = self.cleaned_data['score']
            existed_uni_score.save(update_fields = ['score'])
        except UniversityScore.DoesNotExist:
            university_score.save(university = university)
        return university_score

    class Meta: 
        model = UniversityScore
        exclude = ['score_by_category']