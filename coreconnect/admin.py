from django.contrib import admin
from .models import Profile,Post,Like,Follower,Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Comment)