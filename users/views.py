from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .forms import LoginForm , UserRegistrationForm , UserEditForm , ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile

from posts.models import Post


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data) 
            data = form.cleaned_data #Extracts safe, validated user input from the form.
            user = authenticate(request,username=data['username'],password=data['password']) #Checks the username & password combo against the database.
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('feed')
            else:
                messages.error(request, "Invalid username or password.")    
    else:
        form = LoginForm()
    return render(request,'users/login.html',{'form':form})


@login_required
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = Profile.objects.filter(user=current_user).first()
    return render(request,'users/index.html',{'posts':posts,'profile':profile})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #This tells Django: “Create a User object from the form, but don’t save it to the database yet.”
            new_user.set_password(user_form.cleaned_data['password']) #takes the raw password and hashes it securely using Django’s built-in password hasher.
            new_user.save()
            # Profile.objects.create(user=new_user) #creating profile automatically for the registered user
            messages.success(request, "Registered successfully! Please log in.")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()

    return render(request,'users/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('feed')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,'users/edit.html',{'user_form':user_form, 'profile_form':profile_form})

