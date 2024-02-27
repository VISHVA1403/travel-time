from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, PostCreateView, PostDetailView, CommentCreateView, LikeCreateView, FriendshipCreateView, UserProfileUpdateView, LogoutView ,HomeView,create_profile

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-profile/',create_profile,name= "createprofile"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:post_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/like/create/', LikeCreateView.as_view(), name='create_like'),
    path('friendship/create/', FriendshipCreateView.as_view(), name='create_friendship'),
    # Add more URL patterns as needed
]
