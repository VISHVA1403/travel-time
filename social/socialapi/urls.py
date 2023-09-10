# socialapi/urls.py

from django.urls import path
from .views import UserProfileAPIView, PostListCreateAPIView, PostDetailAPIView,login_user,CommentListCreateAPIView,register_user, CommentDetailAPIView, LikeListCreateAPIView, LikeDetailAPIView, FriendshipListCreateAPIView, FriendshipDetailAPIView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='profile-api'),
    path('post/', PostListCreateAPIView.as_view(), name='post-list-create-api'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail-api'),
    path('comment/', CommentListCreateAPIView.as_view(), name='comment-list-create-api'),
    path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail-api'),
    path('like/', LikeListCreateAPIView.as_view(), name='like-list-create-api'),
    path('like/<int:pk>/', LikeDetailAPIView.as_view(), name='like-detail-api'),
    path('friendship/', FriendshipListCreateAPIView.as_view(), name='friendship-list-create-api'),
    path('friendship/<int:pk>/', FriendshipDetailAPIView.as_view(), name='friendship-detail-api'),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
]
