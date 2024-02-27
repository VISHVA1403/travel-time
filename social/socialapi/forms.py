from django import forms
from .models import UserProfile, Post, Comment, Like, Friendship
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'post', 'location', 'latitude', 'longitude')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = '__all__'

class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = '__all__'
