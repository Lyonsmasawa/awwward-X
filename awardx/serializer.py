from rest_framework import serializers
from .models import Profile, Project

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'profile_photo',  'bio', 'my_link', 'followers', 'location', 'created',)

class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Project
        fields = ('owner', 'title', 'image', 'description', 'link', 'average_design',  'average_usability', 'average_creativity', 'average_content', 'average_score',  'created',)
 