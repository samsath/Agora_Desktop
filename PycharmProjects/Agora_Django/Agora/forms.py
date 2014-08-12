import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Agora_git.functions import get_completelist
from Agora_git.models import Repository


class registrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class profileForm(forms.Form):

    firstname = forms.CharField(label="First Name", required=True)
    surname = forms.CharField(label="Last Name", required=True)
    aboutme = forms.CharField(label="About You", required=True, widget=forms.Textarea, max_length=500)
    photo = forms.ImageField(label="Select a photo")
    role = forms.CharField(label="Your Role")

class NewRepoForm(forms.Form):

    reponame = forms.CharField(label="Project Name", required=True, max_length=200, error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores. As well be unique.") })

    def clean_reponame(self):
        value = self.cleaned_data['reponame'].replace(" ", "_")
        try:
            repos = Repository.objects.get(name__iexact=value)
        except Repository.DoesNotExist:
            return value
        raise forms.ValidationError("Project already exists")