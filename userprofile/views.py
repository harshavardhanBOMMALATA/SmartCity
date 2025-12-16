from django.shortcuts import render
from . import profile_api as api
# Create your views here.
def profie_view(request):
    if api.is_user(request) is False:
        return render(request, 'login.html',{'message':'Please log in to view your profile.'})
    return render(request, 'profile.html')
