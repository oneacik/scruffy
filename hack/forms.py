import hashlib

from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm

from hack.models import Project, Hacker


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'privacy', 'people_limit', 'email']

    def clean_people_limit(self):
        pl = self.cleaned_data['people_limit']
        if pl>20 or pl<0:
            raise forms.ValidationError("People value must be beetween 0 and 20")
        return pl

    def clean_email(self):
        email=self.cleaned_data['email']
        if Project.objects.filter(email=email, active=True).exists():
            raise forms.ValidationError("U can't have more than one project activated")
        return email


class JoinForm(forms.Form):
    email = forms.EmailField()


