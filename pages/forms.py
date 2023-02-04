from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from pages.models import UserProfileModel,Posts
class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField(max_length=250)
    password=forms.CharField(max_length=250)

class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    )
    gender=forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model=UserProfileModel
        exclude=("user",)

        widgets={
            # "user":forms.Select(attrs={'class':'form-control'}),
            "dob":forms.DateInput(attrs={'type':'date'}),
            "bio": forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            "profile_picture":forms.ClearableFileInput(attrs={'class':'form-control-file'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        exclude=("user",)
        fields="__all__"
        widgets={
            "title":forms.TextInput(attrs={'class':'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "post_image":forms.ClearableFileInput(attrs={'class':'form-control-file'}),
            # "user":forms.Select(attrs={'class':'form-control'}),
            # "post_like": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "user": forms.HiddenInput(),
        }