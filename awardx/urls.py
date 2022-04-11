from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('submit-site/', views.submitSite, name="submit-site"),
    path('update-user/', views.updateUser, name="update-user"),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),
    # path('update-post/<str:pk>/', views.updatePost, name="update-post"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('project/<str:pk>/', views.projectPage, name="project"),
    path('logout/', views.logoutUser, name="logout"),
    path('follow/<str:pk>/', views.followForm, name="follow"),
    path('', views.)
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 