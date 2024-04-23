# chat/views.py
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, DocumentForm
from .models import Document  
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from langchain.llms import OpenAI
from .langchain_client import answer_question
from django.conf import settings
from django.http import JsonResponse


def query_documents(request):
    query = request.GET.get('query')
    if query:
        try:
            answer = answer_question(query)
            return JsonResponse({'answer': answer})
        except Exception as e:
            # Log the exception for server-side debugging
            print(f"Error processing query: {str(e)}")
            # Return a JSON error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)


################################################################
################################################################

def chat_home(request):
    course_id = None
    initials = "GU"  # Default initials for Guest User
    if request.user.is_authenticated:
        initials = ''.join([name[0].upper() for name in request.user.get_full_name().split() if name])
        course_id = request.user.course.id if request.user.course else None

    return render(request, 'chat/chatbot.html', {
        'username': request.user.first_name,
        'user_initials': initials,
        'user_course_id': course_id
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

def document_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('DjangoChatbot.views.document_upload'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Render list page with the documents and the form
    return render(
        request,
        'chat/document_upload.html',
        {'form': form}
    )
