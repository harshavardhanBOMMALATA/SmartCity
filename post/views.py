from django.shortcuts import render
from django.http import JsonResponse
import json
from database.views import get_post_by_id
from database import views as db_views
from database.models import Posts,PostVerdict

def post(request):
    return render(request, 'post.html')

def post_detail(request, post_id):
    response=db_views.is_post_available(post_id)
    if response=='0':
        return render(request,'home.html',{'message':'Post unavailable'})
    elif response=='1':
        return render(request,'post.html',{'post_id':post_id})
    
def getpost(request,postId):
    try:
        post=Posts.objects.get(id=postId)
        post={
            'id':post.id,
            'author_email':post.author_email,
            'title':post.title,
            'short_description':post.short_description,
            'description':post.description,
            'location':post.location,
            'time':post.created_at.isoformat() if post.created_at else None,
            'photo':post.photo.url if post.photo else None
            }
        return JsonResponse({'status':'success','post':post})
    except Posts.DoesNotExist:
        return JsonResponse({"message":"not working"})
    
def agree(request,postid):
    return db_views.postagree(request,postid)

def disagree(request,postid):
    return db_views.postdisagree(request,postid)

def result(request,postid):
    return db_views.result(request,postid)

def response(request,postId):
    if(db_views.result(request,postId)):
        return JsonResponse({"response":'true'},status=200)
    else:
        return JsonResponse({"response":"false"},status=403)

def loginornot(request):
    if(request.session.get('email') is None):
        return JsonResponse({"verdict":"false"})
    return JsonResponse({"verdict":"true"})

def verdict(request, postid):
    # Count ALL votes for this post
    pcount = PostVerdict.objects.filter(
        post_id=postid,
        verdict=1
    ).count()

    ncount = PostVerdict.objects.filter(
        post_id=postid,
        verdict=0
    ).count()

    # Decide poll verdict
    if pcount > ncount:
        poll_verdict = True
    elif ncount > pcount:
        poll_verdict = False
    else:
        poll_verdict = None  # tie / pending

    # Official verdict not decided yet
    official_verdict = None  # pending

    return JsonResponse({
        'pollverdict': poll_verdict,
        'officialverdict': official_verdict
    })

def responseverdict(request,postId):
    email=request.session.get('email')
    return JsonResponse({'verdict':PostVerdict.objects.get(email=email,post_id=postId)})




def myposts(request):
    if request.session.get('email') is None:
        return render(request,'login.html')
    return render(request,'myposts.html')

def all_myposts(request):
    if request.session.get('email') is None:
        return JsonResponse({'all_my_posts': []}, status=200)

    email = request.session.get('email')
    return db_views.get_my_posts(request, email)
