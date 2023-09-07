from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import json
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *



def home(request):
    return render(request,'base.html')

def ProfilePage(request, pk):
    user_profiles =UserProfile.objects.get(pk=pk)
    context = {
        'user_profiles': user_profiles
    }
    return render(request,'Profilepage.html', context)

def myprofile(request):
    user_profiles =UserProfile.objects.get(pk = request.user.id)
    context = {
        'user_profiles': user_profiles
    }
    return render(request,'Profilepage.html', context)

def users(request):
    obj = User.objects.all()
    context = {
        'details': obj
    }
    return render(request, 'Profile.html', context)

def EditProfile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Retrieve the user instance using the pk
            profile.user = request.user
            
            profile.save()
            return redirect('myprofile')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'CreateProfile.html', {'form': form})


def CreateUser(request):
    if(request.method =='POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('home')
    form = UserCreationForm()
    return render(request,'register/createuser.html',{'form':form})

def userlogin(request):
    if (request.method=='POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User not Found')
            return redirect('login')

        user = authenticate(username=username ,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
            return redirect('login')
    context={}
    return render(request,'register/login.html',context)

def userlogout(request):
    logout(request)
    return redirect('login')

def Userdetailapi(request):
    datas = User.objects.all()
    return JsonResponse({'data':"ihijojweij"})

print("hello")
print("hi")
