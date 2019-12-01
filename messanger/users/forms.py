from django.forms import ModelForm
from users.models import User
from django.contrib.auth.forms import UserCreationForm

class UserNewForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
