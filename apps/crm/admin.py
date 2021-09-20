from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import MyUser, Company, Project, ContactMessage


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'is_manager')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'is_manager')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username', 'email', 'is_staff', 'is_superuser', 'is_manager', 'first_name', 'last_name', 'profile_picture')
    list_editable = ('is_staff', 'is_superuser', 'is_manager',)
    list_filter = ('is_manager',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Settings', {'fields': ('email', 'first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_manager')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class CompanyAdminForm(forms.ModelForm):
    sh_description = forms.CharField(widget=CKEditorUploadingWidget, )
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = Company
        fields = (
            'name', 'contact', 'sh_description', 'description', 'address', 'phone', 'ad_phone_1', 'ad_phone_2', 'email',
            'ad_email_1', 'ad_email_2', 'created_by', 'updated_by')


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm
    add_form = CompanyAdminForm
    fields = (
        'name', 'contact', 'sh_description', 'description', 'address', 'phone', 'ad_phone_1', 'ad_phone_2', 'email',
        'ad_email_1', 'ad_email_2', 'created_by', 'updated_by')
    list_display = ('name', 'contact', 'date_of_create', 'date_of_change', 'created_by', 'updated_by')
    list_display_links = ('name',)

    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = Project
        fields = (
            'name', 'company', 'description', 'start_date', 'end_date', 'price', 'created_by', 'updated_by')


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    add_form = ProjectAdminForm
    fields = (
        'name', 'company', 'description', 'start_date', 'end_date', 'price', 'created_by', 'updated_by')
    list_display = ('name', 'company', 'start_date', 'end_date', 'price', 'created_by', 'updated_by')
    list_display_links = ('name',)

    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class ContactMessageAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget, )

    class Meta:
        model = ContactMessage
        fields = ('title', 'project', 'type_of_message',  'description',)


class ContactMessageAdmin(admin.ModelAdmin):
    form = ContactMessageAdminForm
    add_form = ContactMessageAdminForm
    fields = (
        'title', 'project', 'type_of_message', 'description', 'manager')
    list_display = ('title', 'project', 'company', 'type_of_message', 'date', 'manager')
    list_display_links = ('title',)

    def save_model(self, request, obj, form, change):
        if obj.manager is None:
            obj.manager = request.user
        obj.company = obj.project.company
        obj.save()


# class LikesAdmin(admin.ModelAdmin):
#     fields = ('liked_by', 'liked_contact_message', 'like',)
#     list_display = ('liked_contact_message', 'liked_by', 'like', 'created')
#     list_editable = ('like',)

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
# admin.site.register(Likes, LikesAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
