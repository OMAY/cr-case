from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import get_user_model
from apps.crm.models import MyUser, Company, Project, ContactMessage

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


class ProjectModelForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = Project
        fields = (
            'name',
            'company',
            'description',
            'start_date',
            'end_date',
            'price',
        )


class ContactMessageModelForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = ContactMessage
        fields = (
            'title',
            'project',
            'type_of_message',
            'description',
        )

class CompanyModelForm(forms.ModelForm):
    sh_description = forms.CharField(widget=CKEditorUploadingWidget, )
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = Company
        fields = (
            'name',
            'contact',
            'sh_description',
            'description',
            'address',
            'phone',
            'ad_phone_1',
            'ad_phone_2',
            'email',
            'ad_email_1',
            'ad_email_2',
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

