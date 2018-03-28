from django import forms

class ScoreForm(forms.ModelForm):
    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 10:
            raise forms.ValidationError(
                "Score is greater equal than 0 or lower equal than 10",
                code="invalid_score"
            )
        else:
            score = round(score, 2)
        return score
