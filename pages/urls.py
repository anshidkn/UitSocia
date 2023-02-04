from django.urls import path,include
from pages import views
urlpatterns=[
    path("register",views.SignUpView.as_view(),name="register"),
    path("login",views.SiginView.as_view(),name="login"),
    path("home",views.IndexView.as_view(),name="home"),
    path("add/profile",views.UserProfileCreateView.as_view(),name="profile-create"),
    path("profile/list",views.UserProfileListView.as_view(),name="profile-list"),
    path("logout",views.signout_view,name="logout"),
    path("add/post",views.AddPostView.as_view(),name="post-add"),
    path("home/<int:id>/delete",views.PostDeleteView.as_view(),name="post-delete")
    # path("post/list",views.PostListView.as_view(),name="post-list"),

]
