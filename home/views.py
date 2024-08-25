from account.models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
def getUsers(request):
    if request.user.role == 'Admin':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('base:dashboard')

    getUsers = User.objects.all().order_by('-created_at')

    context = {
        'getUsers': getUsers
    }

    return render(request, 'pages/users/index.html', context)

@login_required
def addUser(request):
    return render(request, 'pages/users/create.html');