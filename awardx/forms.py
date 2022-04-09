import imp
from django import forms
from .models import Follow, Profile, Project

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
