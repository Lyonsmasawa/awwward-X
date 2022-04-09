import imp
from django import forms
from .models import Follow, Profile, Project
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FollowForm(forms.ModelForm):
    """Form definition for FollowForm."""

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Follow
        fields = '__all__'
        exclude = ['whoIsFollowing', 'whoToFollow'] 

class UnFollowForm(forms.ModelForm):
    """Form definition for MODELNAME."""

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Follow
        fields = '__all__'
        exclude = ['whoIsFollowing', 'whoToFollow']

class ProjectForm(forms.ModelForm):
    """Form definition for Project."""

    class Meta:
        """Meta definition for Projectform."""

        model = Project
        fields = '__all__'
        exclude = ['owner']

class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""

    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        fields = '__all__'
        exclude = ['user', 'followers', 'following',]




