from django.forms import ModelForm

class ScoreForm(ModelForm):
    @property
    def model(self):
        return self._meta.model
        