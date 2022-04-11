from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Project, Rating, Follow

# Create your tests here.
class ProfileTestClass(TestCase):
    def setUp(self):
        self.new_obj = User(username = "new_obj", email = "new_obj@gmail.com",password = "pass")
        self.profile = Profile(bio='bio', user= self.new_obj)
        self.new_obj.save()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_obj, User))
        self.assertTrue(isinstance(self.profile, Profile))


class ProjectTestClass(TestCase):
    def setUp(self):
        self.new_obj = User(username = "new_obj", email = "new_obj@gmail.com",password = "pass")
        self.profile = Profile(bio='bio', user= self.new_obj)

        self.project = Project(image = 'imageurl', name ='img', description = 'img-cap', profile = self.profile)
        
        self.new_obj.save()
        self.profile.save()
        self.project.save()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.img, Project))

    def test_save(self):
        projects = Project.objects.all()
        self.assertTrue(len(projects)> 0)

    def test_delete(self):
        projects = Project.objects.all()
        self.assertEqual(len(projects),1)
        self.project.delete()
        new_list = Project.objects.all()
        self.assertEqual(len(new_list),0)

class FollowTestClass(TestCase):
    def setUp(self):
        self.new_obj = User(username = "new_obj", email = "new_obj@gmail.com",password = "pass")
        self.profile = Profile(bio='bio', user= self.new_obj)

        self.two = User(username = "two", email = "two@gmail.com",password = "pass")
        self.profile2 = Profile(bio='bio', user= self.two) 

        self.new.save()
        self.two.save()

        self.follow = Follow (whoIsFollowing = self.profile, WhoToFollow = self.two )
        
    def tearDown(self):
        Profile.objects.all().delete()        
        User.objects.all().delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.follow,Follow))

class RatingTestClass(TestCase):
    def setUp(self):
        self.new_obj = User(username = "new_obj", email = "new_obj@gmail.com",password = "pass")
        self.profile = Profile(bio='bio', user= self.new_obj)

        self.project = Project(image = 'imageurl', name ='img', description = 'img-cap', profile = self.profile)

        self.rating = Rating(user=self.new_obj, project=self.project, design= 10,  usability= 10, content = 10, creativity = 10, average = 10)
        self.new_obj.save()
        self.profile.save()
        self.project.save()
        self.rating.save()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Rating.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save(self):
        ratings = Rating.objects.all()
        self.assertTrue(len(ratings)> 0)

    def test_delete(self):
        ratings = Project.objects.all()
        self.assertEqual(len(ratings),1)
        self.rating.delete()
        new_list = Rating.objects.all()
        self.assertEqual(len(new_list),0)