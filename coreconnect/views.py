import datetime
import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.models import User
from coreconnect.models import Profile,Post,Like,Follower,Comment
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
   profile=Profile.objects.get(user=request.user)
   post_feed=Post.objects.all()
   comments=Comment.objects.all()
   return render(request,'index.html',{'post_feed':post_feed,'profile':profile,'comments':comments})

def register(request):
    if request.method == 'POST':
       username=request.POST['username']
       email=request.POST['email']
       password1=request.POST['password1']
       password2=request.POST['password2']

       if password1 == password2:
           if User.objects.filter(username=username).exists():
              messages.info(request,'username is already taken')
              return redirect('signup')
           elif User.objects.filter(email=email).exists():
              messages.info(request,'email already taken')
              return redirect('signup')
           else:
              new_user=User.objects.create_user(username=username,email=email,password=password1)
              new_user.save()
                 
              #log user in and redirect to setting page
              user_login= auth.authenticate(username=username,password=password1)
              auth.login(request,user_login)

              #creating profile for new user
              user_model=User.objects.get(username=username)
              new_profile=Profile.objects.create(user=user_model,dob=datetime.date.today())
              new_profile.save()

              return redirect('setting')
       else:    
         messages.info(request,'Password not matching')
         return redirect('signup')

    else:
      return render(request,'signup.html')
    

def signin(request):
   if request.method == 'POST':
       username=request.POST['username']
       password=request.POST['password']

       user= auth.authenticate(username=username,password=password)

       if user is not None:
          auth.login(request,user)
          return redirect('/')
       else:
          messages.info(request,"invalid credentials")
          return redirect('signin')
      
   else:
      return render(request,'signin.html')

@login_required(login_url='signin')
def profile(request,pk):
   user_object = User.objects.get(username=pk)
   user_profile = Profile.objects.get(user=user_object)
   user_post = Post.objects.filter(user=pk)  
   post_size = len(user_post)

   follow=request.user.username
   user=pk
   if Follower.objects.filter(follow=follow, user=user).exists():
    button_text = 'Unfollow'
   else:
    button_text = 'Follow'


   user_follower=len(Follower.objects.filter(user=pk))
   user_following=len(Follower.objects.filter(follow=pk))
   context={
      'user_object':user_object,
      'user_profile':user_profile,
      'user_post':user_post,
      'user_follower':user_follower,   
      'user_following':user_following, 
      'button_text':button_text,
      'post_size':post_size   

   }
   return render(request,'profile.html',context)


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return render(request,"signin.html")

@login_required(login_url='signin')
def setting(request):
   user_profile = Profile.objects.get(user=request.user)

   if request.method == 'POST':

      if request.FILES.get('image') == None:
         image=user_profile.profile_picture
         bio=request.POST['bio']
         dob=request.POST['dob']
         phone_number=request.POST['phonenumber']

         # convert dob string to date object
         dob = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

         # validate dob
         today = datetime.date.today()
         age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
         if age < 18:
                messages.error(request, 'You must be at least 18 years old')
                return redirect('setting')
         user_profile.dob=dob

         user_profile.save()

         # Validate phone number
         phone_regex = r'^\d{10}$'
         if not re.match(phone_regex, phone_number):
            messages.error(request, "Phone number should be 10 digits")
            return redirect('setting')

         user_profile.profile_picture=image
         user_profile.bio=bio
         user_profile.dob=dob
         user_profile.phone_number=phone_number
         user_profile.save()

      if request.FILES.get('image') != None:
         image=request.FILES.get('image')
         bio=request.POST['bio']
         dob=request.POST['dob']
         phone_number=request.POST['phonenumber']

         # convert dob string to date object
         dob = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

         # validate dob
         today = datetime.date.today()
         age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
         if age < 18:
                messages.error(request, 'You must be at least 18 years old')
                return redirect('setting')
         user_profile.dob=dob

         user_profile.save()

         # Validate phone number
         phone_regex = r'^\d{10}$'
         if not re.match(phone_regex, phone_number):
            messages.error(request, "Phone number should be 10 digits")
            return redirect('setting')

         user_profile.profile_picture=image
         user_profile.bio=bio
         user_profile.dob=dob
         user_profile.phone_number=phone_number
         user_profile.save()
      
      return redirect('setting')
   
   return render(request,'setting.html',{'user_profile':user_profile})


@login_required(login_url='signin')
def upload(request):
   if request.method == 'POST':
      user=request.user.username
      image=request.FILES.get('image')
      caption=request.POST['caption']

      new_post = Post.objects.create(user=user,image=image,caption=caption)
      new_post.save()
      return redirect('/')
   else:
      return redirect('/')

def post_like(request):
   like_id = request.GET.get('post_id')
   username=request.user.username
   post=Post.objects.get(post_id=like_id)

   like_filter=Like.objects.filter(username=username,like_id=like_id).first()
   
   if like_filter == None:
        new_like=Like.objects.create(username=username,like_id=like_id)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')
   else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def comment(request):
    if request.method == 'POST':
        user=request.user
        post_id=request.POST['post_id']
        comment=request.POST['comment']
        new_comment=Comment.objects.create(comment=comment,user=user,post_id=post_id)
        new_comment.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follow = request.user.username
        user = request.POST['user']
        print('follow:', follow)
        print('user:', user)

        if Follower.objects.filter(follow=follow,user=user).first():
            delete_follow = Follower.objects.get(follow=follow,user=user)
            delete_follow.delete()
            return redirect('/profile/'+user)
        else:
            new_follow = Follower.objects.create(follow=follow,user=user)
            new_follow.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

def delete_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    if post.user == request.user.username:
        post.delete()
    return redirect('/profile/'+request.user.username)