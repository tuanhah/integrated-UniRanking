from django import forms

class ScoreForm(forms.ModelForm):
    error_messages = {
        'score' : {
            'invalid_score' : "Score is greater equal than 0 or lower equal than 10"
        }
    }

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 10:
            raise forms.ValidationError(
                self.error_messages['score']['invalid_score'],
                code="invalid_score"
            )
        return score
