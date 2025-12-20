from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("HELLO ✔ SMARTCITY VIEW WORKING")

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def signout(request):
    try:
        if(request.session is not None):
                request.session.flush()
    except KeyError:
        pass
    return render(request, 'login.html')