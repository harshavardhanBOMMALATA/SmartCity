from django.shortcuts import render

# Create your views here.
def new_post(request):
    return render(request, 'new_post.html')