from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = CloudinaryField('image', blank=True)
    bio = models.TextField()
    my_link = models.URLField()
    followers = models.IntegerField(blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=20, null = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #auto_now takes a snapshot everytime a save occures while auto_now_add takes a snapshot only one the first time a save occures
   
    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-updated', '-created']

    def __str__(self):
        """Unicode representation of Profile."""
        return str(self.user)

class Project(models.Model):
    """Model definition for Project."""

    # TODO: Define fields here
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    image = CloudinaryField('image')
    image2 = CloudinaryField('image')
    description = models.TextField()
    link = models.URLField()
    location = models.CharField(max_length=20)
    average_design = models.FloatField(blank=True, null=True)
    average_usability = models.FloatField(blank=True, null=True)
    average_creativity = models.FloatField(blank=True, null=True)
    average_content = models.FloatField( blank=True, null=True)
    average_score = models.FloatField( blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) #auto_now takes a snapshot everytime a save occures while auto_now_add takes a snapshot only one the first time a save occures
   

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-updated', '-created']

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

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Rating(models.Model):
    """Model definition for Rating."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    design = IntegerRangeField(min_value=1, max_value=10, null=True)
    usability = IntegerRangeField(min_value=1, max_value=10, null=True)
    content = IntegerRangeField(min_value=1, max_value=10, null=True)
    creativity = IntegerRangeField(min_value=1, max_value=10, null=True)
    average = models.FloatField(null=True)
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Rating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-when']

    def __str__(self):
        """Unicode representation of Rating."""
        return str(self.project)
