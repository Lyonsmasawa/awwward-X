from django.shortcuts import render
from .models import Follow, Profile, Project
from .forms import UnFollowForm, FollowForm

# Create your views here.
def home(request):
    projects = Project.objects.all()

    context = {'projects': projects, }
    return render(request, 'awardx/home.html', context)

def profile(request, pk):
    user = Profile.objects.get(id = pk)
    user_projects = user.project_set.all()
    form = FollowForm()

    whoIsFollowing = Profile.objects.get(user = request.user)
    whoToFollow = Profile.objects.get(user = user.id) #lyons1
    
    if request.method == 'POST':
        if 'follow' in request.POST:
            form = FollowForm(request.POST)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.whoToFollow = whoToFollow
                form_data.whoIsFollowing = whoIsFollowing
                form_data.save()
                
                get_followers = Follow.objects.filter(whoToFollow = whoToFollow)
                followers_count = get_followers.count()

                whoToFollow.followers = followers_count
                whoToFollow.save()

                get_following = Follow.objects.filter(whoIsFollowing = whoIsFollowing)
                follow_count
                




    project_count = user_projects.count()

    context = {'user': user, 'user_projects': user_projects, 'project_count':project_count, 'follow_form': form,}
    return render(request, 'awardx/profile.html', context)