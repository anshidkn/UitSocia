from django.urls import path
from .import views

urlpatterns =[
    path('',views.index,name='index'),
    path('signup',views.register,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('setting',views.setting,name='setting'),
    path('upload',views.upload,name='upload'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('post-like',views.post_like,name='post-like'),
    path('comment',views.comment,name='comment'),
    path('follow',views.follow,name='follow'),
    path('delete_post/<int:post_id>/',views.delete_post, name='delete_post'),
]