from django.urls import path
from . import views


urlpatterns =[
    path('',views.home,name='home'),
    path('profile/<int:pk>/', views.ProfilePage, name='profile'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('users',views.users,name="users"),
    path('profilecreate',views.EditProfile,name="create_profile"),
    path('create-user',views.CreateUser,name = 'create-user'),
    path('loginuser',views.userlogin,name='login'),
    path('logoutuser',views.userlogout,name='logout'),
    path("Detailapi",views.Userdetailapi,name='firstapi'),
]