# import uuid
from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField()
    dob=models.DateField(default=date.today)
    phone_number=models.CharField(max_length=250)
    profile_picture=models.ImageField(upload_to="profile_images",default='default.jpg')
    

    def __str__(self):
        return self.user.username

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user=models.CharField(max_length=100)
    caption=models.TextField()
    image=models.ImageField(upload_to='post_images')
    created_at=models.DateTimeField(auto_now_add=True)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return  self.user

    @property
    def post_user(self):
        return User.objects.get(username=self.user)


class Like(models.Model):
    like_id=models.CharField(max_length=100)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Follower(models.Model):
    user=models.CharField(max_length=100)
    follow=models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def post_user(self):
    #     profile = Profile.objects.get(user=self.user)
    #     return {'username': self.user.username, 'profile_picture': profile.profile_picture.url}

    def __str__(self):
        return self.comment
