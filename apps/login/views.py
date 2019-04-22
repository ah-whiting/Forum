from django.shortcuts import render, redirect
import bcrypt
from .models import User
from django.contrib import messages
from django.http import JsonResponse

def create_user(request):
    e = User.objects.validator(request.POST)
    if len(e) > 0:
        for key, value in e.items():
            messages.error(request, value)
        return redirect('/login')

    user = User.objects.create(
        username = request.POST["username"],
        email = request.POST['email'],
        pass_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['id'] = user.id
    request.session['username'] = user.username
    return redirect('/success')

def login(request):
    if request.method == "GET":
        return render(request, "login/index.html")
        
    e = User.objects.login_validator(request.POST)
    if len(e) > 0:
        for key, value in e.items():
            messages.error(request, value)
        return redirect('/login')
    user = User.objects.get(email = request.POST['email'])
    request.session['id'] = user.id
    request.session['username'] = user.username
    messages.success(request, "Successful Login")
    return redirect ('/success')

def success(request):
    if not 'id' in request.session:
        messages.error(request, "You must log in first")
        return redirect('/login')   
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/login')

def validate_username(request):
    if request.method == 'GET':
        data = {}
        data = {
            'is_taken': User.objects.filter(username__iexact = request.GET['username']).exists()
        }
    return JsonResponse(data)    


