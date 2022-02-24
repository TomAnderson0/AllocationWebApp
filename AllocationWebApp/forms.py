from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, Csv, Project, Instance

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type', 'instance')

class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name',)

class SupervisorProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('instance', 'supervisor', 'title', 'description', 'tags', 'seSuitable')
        widgets = {
            'instance': forms.HiddenInput,
            'supervisor': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super(SupervisorProjectForm, self).__init__(*args, **kwargs)
        self.fields['supervisor'].disabled = True
        self.fields['instance'].disabled = True

class SupervisorProjectUpdate(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('instance', 'supervisor', 'title', 'description', 'tags', 'seSuitable')
        widgets = {
            'instance': forms.HiddenInput,
            'supervisor': forms.HiddenInput,
        }