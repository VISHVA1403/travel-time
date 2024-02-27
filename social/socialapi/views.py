
from rest_framework import generics
from .models import UserProfile, Post, Comment, Like, Friendship
from .serializers import UserProfileSerializer, PostSerializer,LoginSerializer, CommentSerializer, LikeSerializer, FriendshipSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
import json
from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth.models import User

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateAPIView(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeListCreateAPIView(APIView):

    def get(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LikeDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        like = self.get_object(pk)
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    def put(self, request, pk):
        like = self.get_object(pk)
        serializer = LikeSerializer(like, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        like = self.get_object(pk)
        like.delete()

class FriendshipListCreateAPIView(generics.ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

class FriendshipDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user (optional)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

# # Template views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import UserForm, LoginForm, UserProfileForm, PostForm, CommentForm, LikeForm, FriendshipForm
from .models import UserProfile, Post, Comment, Like, Friendship
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.hashers import make_password

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to the home page after successful registration
        else:
            # Handle form errors
            return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('createprofile')  # Redirect to the home page after successful login
            else:
                error = 'Invalid username or password.'
        else:
            error = 'Form is not valid.'
        return render(request, self.template_name, {'form': form, 'error': error})

# from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')  # Assuming 'profile' is the URL name for the profile page
    else:
        form = UserProfileForm()
    return render(request, 'create_profile.html', {'form': form})

@login_required
def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

class UserProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        return context

class PostCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'create_post.html'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')  # Redirect to the home page after successful post creation
        return render(request, self.template_name, {'form': form})

class PostDetailView(LoginRequiredMixin,TemplateView):
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = kwargs['post_id']
        post = Post.objects.get(id=post_id)
        context['post'] = post
        return context

# Add more views for other functionalities as needed...

class CommentCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'create_comment.html'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = kwargs['post_id']
            comment.save()
            return redirect('post_detail', post_id=kwargs['post_id'])  # Redirect to the post detail page after successful comment creation
        return render(request, self.template_name, {'form': form})

class LikeCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'create_like.html'

    def post(self, request, *args, **kwargs):
        form = LikeForm(request.POST)
        if form.is_valid():
            like = form.save(commit=False)
            like.user = request.user
            like.post_id = kwargs['post_id']
            like.save()
            return redirect('post_detail', post_id=kwargs['post_id'])  # Redirect to the post detail page after successful like creation
        return render(request, self.template_name, {'form': form})

class FriendshipCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'create_friendship.html'

    def post(self, request, *args, **kwargs):
        form = FriendshipForm(request.POST)
        if form.is_valid():
            friendship = form.save(commit=False)
            friendship.user = request.user
            friendship.save()
            return redirect('home')  # Redirect to the home page after successful friendship creation
        return render(request, self.template_name, {'form': form})

class UserProfileUpdateView(LoginRequiredMixin,TemplateView):
    template_name = 'update_profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful profile update
        return render(request, self.template_name, {'form': form})

class LogoutView(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')  # Redirect to the login page after successful logout
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')[:10]