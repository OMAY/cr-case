from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password

from apps.crm.models import MyUser

User = get_user_model()


class MyUserModelForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_picture'
        )


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean(self):
        pass

