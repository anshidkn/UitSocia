from django.db import models
from django.contrib.auth.models import User



class UserProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=250,null=True)
    dob=models.DateField()
    gender = models.CharField(max_length=10)
    phone_number=models.CharField(max_length=250)
    profile_picture=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.user.username
    
    
class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    description=models.TextField()
    post_like=models.ManyToManyField(User,related_name="post_like")
    post_image=models.ImageField(upload_to="images",null=True)
    publish_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    comment_like=models.ManyToManyField(User,related_name="comment_like")

    def __str__(self):
        return self.comment

