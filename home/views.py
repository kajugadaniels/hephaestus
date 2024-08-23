from django.shortcuts import render

def dashboard(request):
    return render(request, 'pages/dashboard.html')

def getUsers(request):
    return render(request, 'pages/users/index.html')