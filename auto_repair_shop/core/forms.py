
from django import forms
from django.contrib.auth.forms import UserCreationForm as UCF, UserChangeForm

from .models import User, UserCar


class UserCreationForm(UCF):

    class Meta(UCF):
        model = User
        fields = tuple()


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = tuple()


class UserRegisterForm(UCF):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserCarUpdateForm(forms.ModelForm):

    class Meta:
        model = UserCar
        fields = ['model', 'plate_num']
