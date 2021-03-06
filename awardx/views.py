from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Follow, Profile, Project, Rating
from .forms import ProfileForm, ProjectForm, RatingForm, UnFollowForm, FollowForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from .forms import CustomUserForm
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import  ProfileSerializer, ProjectSerializer

# Create your views here.
def home(request):
    projects = Project.objects.all()
    date = datetime.date.today()

    q = request.GET.get('q')
    if request.GET.get('q') != None:
        projects = Project.objects.filter(
            Q(title__icontains = q) |
            Q(owner__user__username__icontains = q) 
        )
        searched_count = projects.count()
        q=True
        today = True
        best = False

    else:
        get_by_score = Project.objects.filter(created__contains = date).order_by('-average_score')
        project_list = []
        if get_by_score.count() > 0:
            for project in get_by_score:
                if project.average_score is not None:
                    project_list.append(project)
                    print(project.average_score)

            if len(project_list) > 0:
                best = project_list[0]
                print(best.average_score)
                searched_count = False
                q = False
                today = True

            else:
                best = False
                searched_count = False 
                q = False
                today = False
        else:
            best = False
            today = False
            q = False
            searched_count = False
           
        
        
    context = {'projects': projects, 'best':best, 'date':date, 'today':today, 'q':q, 'pq':searched_count, }
    return render(request, 'awardx/home.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            Profile.objects.create(user = user)

            login(request, user) 
            return redirect('home')

        else:
            messages.error(request, 'please try again')
    else:
        form = CustomUserForm()

    context = {'form': form}
    return render(request, 'awardx/login_register.html', context) 

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

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

def logoutUser(request):
    logout(request)
    return redirect('home')

def profile(request, pk):
    # user = Profile.objects.get(id = pk)
    user = get_object_or_404(Profile, pk=pk)
    user_projects = user.project_set.all()
    follow_form = FollowForm()
    unfollow_form = UnFollowForm()

    if request.user.is_authenticated:
        whoIsFollowing = Profile.objects.get(user = request.user)
        whoToFollow = Profile.objects.get(user = user.id)
        isFollowing = Follow.objects.filter(whoIsFollowing=whoIsFollowing, whoToFollow=whoToFollow)
    
    else:
        isFollowing = False

    project_count = user_projects.count()

    context = {'user': user, 'user_projects': user_projects, 'project_count':project_count, 'isFollowing':isFollowing, 'follow_form': follow_form, 'unfollow_form': unfollow_form,}
    return render(request, 'awardx/profile.html', context)

@login_required(login_url='login')
def followForm(request, pk):
    user = get_object_or_404(Profile, pk=pk)
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

    context = {}
    return render(request, 'awardx/profile.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

def projectPage(request, pk):
    project = Project.objects.get(id = pk)
    ratings = Rating.objects.filter(project = project)
    form = RatingForm()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.project = project
            data.average = (data.design + data.usability + data.content+data.creativity)/4
            data.save()
            return redirect( 'project', pk) 
    

    raters = []
    design_ratings = []
    usability_ratings = []
    content_ratings = []
    creativity_ratings = []
    average = []

    for rating in ratings:
        raters.append(rating.user)
        design_ratings.append(rating.design)
        usability_ratings.append(rating.usability)
        content_ratings.append(rating.content)
        creativity_ratings.append(rating.creativity)
        average.append(rating.average)

    ratings_count = ratings.count()

    if ratings_count > 0:
        project.average_design = sum(design_ratings)/ratings_count
        project.average_usability = sum(usability_ratings)/ratings_count
        project.average_content = sum(content_ratings)/ratings_count
        project.average_creativity = sum(creativity_ratings)/ratings_count

        total_average = sum(average)/ratings_count
        project.average_score = total_average
        project.save()

    else:
        form = RatingForm()
    
    context = {'project': project, 'form': form, 'ratings':ratings, 'ratings_count':ratings_count, 'raters':raters,}
    return render(request, 'awardx/project.html', context)

@login_required(login_url='login')
def deletePost(request, pk):
    project = Project.objects.get(id=pk)

    if request.user != project.owner.user:
        return HttpResponse('This method is restricted')

    if request.method == 'POST':
        project.delete()
        return redirect('home')
    
    context = {'obj':project}
    return render(request, 'awardx/delete.html', context)

def search(request): 
    pass

# def updatePost(request, pk):
#     project = Project.objects.get(id = pk)

#     if request.method == 'POST':
#         form = ProjectForm(request.POST, request.FILES, instance=project)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

#     else:
#         form = ProjectForm(instance= project)

#     context = {'form': form, }
#     return render(request, 'awardx/submit_form.html', context)

class profileList(APIView):

    def get(self ,request, format = None):
        all_profiles =  Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        
        return Response(serializers.data) 

class projectList(APIView):

    def get(self, request, format = None):
        all_projects =  Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)

        return Response(serializers.data)  