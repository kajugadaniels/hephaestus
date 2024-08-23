from django.shortcuts import render
from account.models import *

def dashboard(request):
    return render(request, 'pages/dashboard.html')

def getUsers(request):
    getUsers = User.objects.all()

    context = {
        'getUsers': getUsers
    }

    return render(request, 'pages/users/index.html', context)