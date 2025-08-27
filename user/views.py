from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from .forms import LoginForm , RegisterForm ,ProfileForm
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect('home')  # change 'home' to your home URL name
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'views/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # creates the user
            except IntegrityError:
                # In case your form doesn’t already validate unique fields
                messages.error(request, "That username or email is already in use.")
            else:
                login(request, user)  # auto-login
                messages.success(request, "Your account has been created successfully!")
                return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    # Make sure this template actually exists at templates/views/register.html
    return render(request, "views/register.html", {"form": form, "active_page": "register"})



@login_required
def profile_view(request):
    # Get or create profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("profile")  # use your url name
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "views/profile.html", {"form": form, "active_page": "profile"})