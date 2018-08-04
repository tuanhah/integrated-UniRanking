from django.contrib.auth.forms import UserCreationForm

UserModel = UserCreationForm.Meta.model

class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name','username','email')
