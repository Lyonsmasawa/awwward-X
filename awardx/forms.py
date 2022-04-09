import imp
from django import forms
from .models import Follow

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
