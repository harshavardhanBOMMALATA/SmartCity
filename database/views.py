from database.models import Users,Posts
from django.http import HttpResponse,JsonResponse

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