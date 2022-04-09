from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Follow, Profile, Project
from .forms import ProfileForm, ProjectForm, UnFollowForm, FollowForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from .forms import CustomUserForm

# Create your views here.
def home(request):
    projects = Project.objects.all()

    context = {'projects': projects, }
    return render(request, 'awardx/home.html', context)

def registrationPage(request):

    context = {}
    return render(request, 'awardx/login_register.html', context) 

def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or Password')

    context = {'page': page}
    return render(request, 'awardx/login_register.html', context) 


def profile(request, pk):
    user = Profile.objects.get(id = pk)
    user_projects = user.project_set.all()

    whoIsFollowing = Profile.objects.get(user = request.user)
    whoToFollow = Profile.objects.get(user = user.id)
    
    isFollowing = Follow.objects.filter(whoIsFollowing=whoIsFollowing, whoToFollow=whoToFollow)

    if request.method == 'POST':
        if 'follow' in request.POST:
            form = FollowForm(request.POST)
            if form.is_valid():
                #fill the follow model fields
                form_data = form.save(commit=False)
                form_data.whoToFollow = whoToFollow
                form_data.whoIsFollowing = whoIsFollowing
                form_data.save()
                
                #update followed user followers list
                get_followers = Follow.objects.filter(whoToFollow = whoToFollow)
                followers_count = get_followers.count()
                whoToFollow.followers = followers_count
                whoToFollow.save()

                #update current user following list
                get_following = Follow.objects.filter(whoIsFollowing = whoIsFollowing)
                following_count = get_following.count()
                whoIsFollowing.following = following_count
                whoIsFollowing.save()
            
            return redirect('profile', user.id)

        elif 'unfollow' in request.POST:
            form = UnFollowForm(request.POST)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data = Follow.objects.filter(whoIsFollowing=whoIsFollowing, whoToFollow=whoToFollow)
                form_data.delete()

                #update un-followed user followers list
                get_followers = Follow.objects.filter(whoToFollow = whoToFollow)
                followers_count = get_followers.count()
                whoToFollow.followers = followers_count
                whoToFollow.save()

                #update current user following list
                get_following = Follow.objects.filter(whoIsFollowing = whoIsFollowing)
                following_count = get_following.count()
                whoIsFollowing.following = following_count
                whoIsFollowing.save()
            return redirect('profile', user.id)
    else:
        follow_form = FollowForm()
        unfollow_form = UnFollowForm()

    project_count = user_projects.count()

    context = {'user': user, 'user_projects': user_projects, 'isFollowing':isFollowing, 'project_count':project_count, 'follow_form': follow_form, 'unfollow_form': unfollow_form, }
    return render(request, 'awardx/profile.html', context)

def updateUser(request):
    user = request.user.profile
    form = ProfileForm(instance = user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('profile', request.user.profile.id)

    context = {'form':form, 'user':user}
    return render(request, 'awardx/edit_profile.html', context)

def submitSite(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.owner = request.user.profile
            data.save()
            return redirect('home')

    else:
        form = ProjectForm()

    context = {'form': form, }
    return render(request, 'awardx/submit_form.html', context)