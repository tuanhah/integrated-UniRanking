from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class ScoreValidator:
    message = "Score must be number between 0 and 10"
    code =  "invalid"

    def __init__(self, message = None, code = None):
        if message is not None: 
            self.message = message
        if code is not None: 
            self.code = code        

    def __call__(self, value):
        if value < 0 or value > 10:
            raise ValidationError(self.message, self.code)
    def __eq__(self, other):
        return (
            isinstance(other, ScoreValidator) and
            (self.message == other.message) and
            (self.code == other.code)
        )