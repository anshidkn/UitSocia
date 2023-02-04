from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView,DeleteView
from django.urls import reverse_lazy
from pages.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from pages.models import UserProfileModel,Posts
from django.utils.decorators import method_decorator


def login_required(fn):
    def wrapper(request,*a,**k):
        if not request.user.is_authenticated:
            messages.error(request,"You must login ")
            return redirect("login")
        else:
            return fn(request,*a,**k)
    return wrapper


class SignUpView(CreateView):
    template_name="Signup.html"
    form_class= RegistrationForm
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request,"Account has been created")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Account creation failed")
        return super().form_invalid(form)

class SiginView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*a,**k):
        form=LoginForm(request.POST)
        if form.is_valid(): 
            usr=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            us=authenticate(request,username=usr,password=pwd)
            if us:
                login(request,us)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
    def form_valid(self, form):
        messages.success(self.request,"Login Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Invalid account")
        return super().form_invalid(form)

# @method_decorator(login_required,name="dispatch")
# class IndexView(TemplateView):
#     template_name="home.html"

@method_decorator(login_required,name="dispatch")
class UserProfileCreateView(CreateView):
    template_name="addprofile.html"
    form_class=UserProfileForm
    success_url="profile-list"
    def dispatch(self, request, *args, **kwargs):
        if UserProfileModel.objects.filter(user=request.user).exists():
            return redirect("profile-list")
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Succesfully submitted data")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Enter valid data")
        return super().form_invalid(form)

@method_decorator(login_required,name="dispatch")
class UserProfileListView(ListView):
    model=UserProfileModel
    template_name="profilelist.html"
    context_object_name="todos"
    def get_queryset(self):
        return UserProfileModel.objects.filter(user=self.request.user)

def signout_view(request,*a,**k):
    logout(request)
    return redirect("login")
    messages.success(request,"Account has been logout")

@method_decorator(login_required,name="dispatch")
class AddPostView(CreateView):
    template_name="postadd.html"
    form_class=PostForm
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request,"Post successfully added")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"Post creation failed")
        return super().form_invalid(form)

@method_decorator(login_required,name="dispatch")
class IndexView(ListView):
    model=Posts
    template_name="home.html"
    context_object_name="post_list"
    queryset=Posts.objects.all()

@method_decorator(login_required,name="dispatch")
class PostDeleteView(DeleteView):
    model=Posts
    pk_url_kwarg="id"
    success_url=reverse_lazy("post-add")
