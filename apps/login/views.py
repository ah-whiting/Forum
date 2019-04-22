from django.shortcuts import render, redirect
import bcrypt
from .models import User
from django.contrib import messages


# def root(request):
#     if 'id' in request.session:
#         return redirect('/')
#     return render(request, 'login/index.html')

def create_user(request):
    e = User.objects.validator(request.POST)
    if len(e) > 0:
        for key, value in e.items():
            messages.error(request, value)
        return redirect('/login')

    user = User.objects.create(
        username = request.POST["username"],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        pass_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['id'] = user.id
    request.session['first_name'] = user.first_name
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
    request.session['first_name'] = user.first_name
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


