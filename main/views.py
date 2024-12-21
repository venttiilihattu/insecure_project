from django.shortcuts import render
from .models import Note
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import connection


def user_notes(request, user_id):
    # Vulnerable
    notes = Note.objects.filter(owner__id=user_id)
    return render(request, 'notes.html', {'notes': notes})

    # Fix
    #
    # if request.user.is_authenticated:
    #     if request.user.id == user_id:
    #         notes = Note.objects.filter(owner=request.user)
    #         return render(request, 'notes.html', {'notes': notes})
    #     else:
    #         return render(request, 'notes.html', {'notes': []})
    # else:
    #     return render(request, 'notes.html', {'notes': []})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Vulnerable
        User.objects.create(username=username, password=password)
        return redirect('user_notes', user_id=1) 
    return render(request, 'signup.html')

# Fix
#
# if request.method == 'POST':
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = User.objects.create(username=username)
#     user.set_password(password)  # This hashes the password
#     user.save()
#     return redirect('user_notes', user_id=user.id)
#
SECRET_API_KEY = "mysecretplaintextkey"  # Vulnerable

def sensitive_view(request):
    # Vulnerable
    return render(request, 'sensitive.html', {'key': SECRET_API_KEY})

# Fix
#
# import os
# SECRET_API_KEY = os.environ.get('API_KEY', 'fallback-key-if-not-set')
#
# def sensitive_view(request):
#     return render(request, 'sensitive.html', {'key': "Hidden"})

def search_posts(request):
    return render(request, 'search.html', {'results': []})

def protected_page(request):
    return render(request, 'protected.html', {'data': "Protected Content"})

def search_posts(request):
    query = request.GET.get('q', '')
    # Vulnerable
    sql = f"SELECT title, content FROM main_note WHERE title LIKE '%{query}%'"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()

    return render(request, 'search.html', {'results': results})

# Fix
# Use parameterisation or the Django ORM:
# 
# def search_posts(request):
#     query = request.GET.get('q', '')
#     results = Note.objects.filter(title__icontains=query)
#     return render(request, 'search.html', {'results': results})

def protected_page(request):
    # Vulnerable
    sensitive_notes = Note.objects.all()
    return render(request, 'protected.html', {'notes': sensitive_notes})

# Fix:
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def protected_page(request):
#     sensitive_notes = Note.objects.filter(owner=request.user)
#     return render(request, 'protected.html', {'notes': sensitive_notes})

