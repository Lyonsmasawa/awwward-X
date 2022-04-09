from distutils.command.upload import upload
from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profiles/')
    bio = models.TextField()
    my_link = models.URLField()
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #auto_now takes a snapshot everytime a save occures while auto_now_add takes a snapshot only one the first time a save occures
   
    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return str(self.user)

class Project(models.Model):
    """Model definition for Project."""

    # TODO: Define fields here
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='projects/')
    description = models.TextField()
    link = models.URLField()
    location = models.CharField(max_length=20)
    average_design = models.FloatField(default=0)
    average_usability = models.FloatField(default=0)
    average_content = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #auto_now takes a snapshot everytime a save occures while auto_now_add takes a snapshot only one the first time a save occures
   

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        return self.title

class Follow(models.Model):
    """Model definition for Follow."""

    # TODO: Define fields here
    when = models.DateTimeField(auto_now_add=True)
    whoIsFollowing = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follow')
    whoToFollow = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        """Meta definition for Follow."""

        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        """Unicode representation of Follow."""
        return str(self.when)

class Rating(models.Model):
    """Model definition for Rating."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    design = models.IntegerField(default=0)
    usability = models.IntegerField(default=0)
    content = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Rating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        """Unicode representation of Rating."""
        return str(self.when)
