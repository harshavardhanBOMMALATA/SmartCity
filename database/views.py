from urllib import request
from database.models import Users,Posts,PostVerdict
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render


def check_user_credentials(email, password):
    try:
        user=Users.objects.get(email=email)
        if user.password==password:
            return True
        else:
            return False
    except Users.DoesNotExist:
        return False

def register_user(email, name, phonenumber, password, address):
    try:
        user = Users.objects.get(email=email)
        return "2"   # user already exists
    except Users.DoesNotExist:   # FIXED
        try:
            new_user = Users(
                email=email,
                password=password,
                name=name,
                phonenumber=phonenumber,
                address=address
            )
            new_user.save()
            return "0"   # success
        except Exception:
            return "1"   # insert error

def view_posts(request):
    posts = Posts.objects.all()
    content = []

    for post in posts:
        content.append({
            "id": post.id,
            "author_email": post.author_email,
            "title": post.title,
            "shortdescription": post.short_description,
            "description": post.description,
            "location": post.location,
            "time": post.created_at.isoformat() if post.created_at else None,
            "photo": post.photo.url if post.photo else None
        })

    return JsonResponse({"content": content})

def post_creation(post_id,title,description,location,author_email,photo,short_description,time):
    try:
        new_post=Posts(
            id=post_id,
            title=title,
            description=description,
            location=location,
            author_email=author_email,
            photo=photo,
            created_at=time,
            short_description=short_description
        )

        new_post.save()
        return JsonResponse({'status':'success','message':'Post created successfully'},status=201)
    except Exception as e:
        return JsonResponse({'status':'failure','message':str(e)},status=500)
    
def user_details(email):
    try:
        user=Users.objects.get(email=email)
        user_data={
            'email':user.email,
            'name':user.name,
            'phonenumber':user.phonenumber,
            'address':user.address
        }
        return JsonResponse({'status':'success','profile':user_data},status=200)
    except Users.DoesNotExist:
        return JsonResponse({'status':'failure','message':'User does not exist'},status=404)
    
def update_user_profile(email,name,phonenumber,address):
    try:
        user=Users.objects.get(email=email)
        user.name=name
        user.phonenumber=phonenumber
        user.address=address
        user.save()
        return user_details(email)
    except Users.DoesNotExist:
        return JsonResponse({'status':'failure','message':'User does not exist'},status=404)
    except Exception as e:
        return JsonResponse({'status':'failure','message':str(e)},status=500)
    
def get_post_by_id(request,post_id=None):
    post=Posts.objects.get(id=post_id)
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

def is_post_available(post_id):
    if Posts.objects.filter(id=post_id).exists():
        return '1'  # Post is available
    else:
        return '0'  # Post is not available
    
def postagree(request, postid):
    email=request.session.get('email')
    if request.session.get('email') is None:
        return JsonResponse({"message": "login first to vote"}, status=400)
    
    if PostVerdict.objects.filter(email=email,post_id=postid).exists():
        post=PostVerdict.objects.get(email=email,post_id=postid)
        post.verdict=1
        post.save()
    else:
        post = PostVerdict(
            post_id=postid,
            email=request.session.get("email"),
            verdict=1
        )
        post.save()

    pcount = PostVerdict.objects.filter(post_id=postid, verdict=1).count()
    ncount = PostVerdict.objects.filter(post_id=postid, verdict=0).count()

    return JsonResponse({"pcount": pcount, "ncount": ncount})

def postdisagree(request, postid):
    email = request.session.get('email')
    if email is None:
        return JsonResponse({"message": "login first to vote"}, status=400)

    if PostVerdict.objects.filter(email=email, post_id=postid).exists():
        post = PostVerdict.objects.get(email=email, post_id=postid)
        post.verdict = 0
        post.save()
    else:
        post = PostVerdict(
            post_id=postid,
            email=email,
            verdict=0
        )
        post.save()

    pcount = PostVerdict.objects.filter(post_id=postid, verdict=1).count()
    ncount = PostVerdict.objects.filter(post_id=postid, verdict=0).count()

    return JsonResponse({"pcount": pcount, "ncount": ncount})


def response(request, postid):
    if request.session.get('email') is None:
        return False

    email = request.session.get('email')

    if PostVerdict.objects.filter(post_id=postid, email=email).exists():
        return False

    return True

def get_my_posts(request, email):
    posts = Posts.objects.filter(author_email=email)
    all_my_posts = []

    for post in posts:
        all_my_posts.append({
            'id': post.id,
            'author_email': post.author_email,
            'title': post.title,
            'short_description': post.short_description,
            'description': post.description,
            'location': post.location,
            'time': post.created_at.isoformat() if post.created_at else None,
            'photo': post.photo.url if post.photo else None
        })

    return JsonResponse({'all_my_posts':all_my_posts})

def result(request,postid):
    pcount = PostVerdict.objects.filter(post_id=postid, verdict=1).count()
    ncount = PostVerdict.objects.filter(post_id=postid, verdict=0).count()

    return JsonResponse({"pcount": pcount, "ncount": ncount})