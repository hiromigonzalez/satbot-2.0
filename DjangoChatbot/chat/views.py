# chat/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def chat_home(request):
    if request.user.is_authenticated:
        # Assuming the user has a first and last name, split the names to get initials
        initials = ''.join([name[0].upper() for name in request.user.get_full_name().split() if name])
    else:
        initials = "GU"  # Guest User initials, or choose what makes sense for your app
    
    return render(request, 'chat/chatbot.html', {
        'username': request.user.username,
        'user_initials': initials  # Add this line to pass initials to the template
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat:chat_home')  # Use your 'chat' namespace here
            else:
                return render(request, 'chat/login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat:chat_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})
