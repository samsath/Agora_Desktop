import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Agora.models import Repository


class registrationForm(forms.Form):
    """
    Form for the registration of new user's the basic.
    With a password check to make sure they are the same.
    """

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
    """
    This is the profile input so to have the user name and profile image with other info relatted to them personally
    """

    firstname = forms.CharField(label="First Name", required=True)
    surname = forms.CharField(label="Last Name", required=True)
    aboutme = forms.CharField(label="About You", required=True, widget=forms.Textarea, max_length=500)
    photo = forms.ImageField(label="Select a photo")
    role = forms.CharField(label="Your Role")

class NewRepoForm(forms.Form):
    """
    This is to create a new project so it very basic and just a single input.
    """

    reponame = forms.CharField(label="Project Name", required=True, max_length=200, error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores. As well be unique.") })

    def clean_reponame(self):
        value = self.cleaned_data['reponame'].replace(" ", "_")
        try:
            repos = Repository.objects.get(name__iexact=value)
        except Repository.DoesNotExist:
            return value
        raise forms.ValidationError("Project already exists")


class NoteForm(forms.Form):
    """
    The form for the note so is used to create and edit the notes.
    """

    content = forms.CharField(label="Note", widget=forms.Textarea, required=False)
    bg_colour = forms.CharField(max_length=9, required=False)
    tx_colour = forms.CharField(max_length=9, required=False)



class NoteCommentForm(forms.Form):
    """
    This is the comment section of the note.
    """
    user = forms.CharField(label="name", required=False)
    comment = forms.CharField(label="Comment", widget=forms.Textarea, required=False)
