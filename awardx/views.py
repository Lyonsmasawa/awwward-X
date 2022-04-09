from django.shortcuts import render
from .models import Profile, Project
from .forms import UnFollowForm, FollowForm

# Create your views here.
def home(request):
    projects = Project.objects.all()

    context = {'projects': projects, }
    return render(request, 'awardx/home.html', context)

def profile(request, pk):
    user = Profile.objects.get(id = pk)
    user_projects = user.project_set.all()

    project_count = user_projects.count()

    context = {'user': user, 'user_projects': user_projects, 'project_count':project_count,}
    return render(request, 'awardx/profile.html', context)