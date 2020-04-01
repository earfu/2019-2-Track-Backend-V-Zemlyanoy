from django.forms import ModelForm
from users.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from captcha.fields import CaptchaField

class UserNewForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class UserLoginForm(AuthenticationForm):
    captcha = CaptchaField()
