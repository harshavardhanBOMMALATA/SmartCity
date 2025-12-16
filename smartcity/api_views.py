from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from database.views import check_user_credentials,register_user,post_creation
from database import views as db_views
import random
from database.models import Users, Posts

@csrf_exempt
def login_api(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            email=data.get('email')
            password=data.get('password')
            if(check_user_credentials(email,password)):
                request.session['user_email']=email
                return JsonResponse({'status':'success','message':'Login successful'},status=200)
            else:
                return JsonResponse({'status':'failure','message':'Invalid credentials'},status=401)
        except Exception as e:
            return JsonResponse({'status':'error','message':str(e)},status=400)
    else:
        return JsonResponse({'status':'error','message':'Invalid request method'},status=405)  
    
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            name = data.get('name')
            phonenumber = data.get('phonenumber', '')
            password = data.get('password')
            address = data.get('address', '')

            result = register_user(email, name, phonenumber, password, address)

            if result == "0":
                return JsonResponse(
                    {'status': 'success', 'message': 'Signup successful'},
                    status=201
                )
            elif result == "2":
                return JsonResponse(
                    {'status': 'exists', 'message': 'User already exists'},
                    status=409
                )
            else:
                return JsonResponse(
                    {'status': 'failure', 'message': 'Error during registration'},
                    status=500
                )

        except Exception as e:
            return JsonResponse(
                {'status': 'failure', 'message': str(e)},
                status=400
            )

    return JsonResponse(
        {'status': 'failure', 'message': 'Invalid request method'},
        status=405
    ) 

def posts(request):
    sample_posts = [
        {
            'id': 1,
            'title': 'Community Clean-Up Event',
            'content': 'Join us this Saturday for a community clean-up event at the central park.',
            'author': 'John Doe',
            'date_posted': '2024-06-01'
        },
        {
            'id': 2,
            'title': 'New Bike Lanes Installed',
            'content': 'The city has installed new bike lanes on Main Street to promote eco-friendly transportation.',
            'author': 'Jane Smith',
            'date_posted': '2024-06-02'
        }
    ]
    return db_views.view_posts(request)

@csrf_exempt
def new_post(request):
    email=request.session.get('user_email','')
    if(email==""):
        return JsonResponse({'status':'logout','message':'User not logged in'},status=401)
    post_id=random.randint(1000,9999)
    while(Posts.objects.filter(id=post_id).exists()):
        post_id=random.randint(1000,9999)
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            title=data.get('title')
            description=data.get('description')
            short_description=data.get('short_description','')
            location=data.get('location','')
            time=data.get('time','')
            photo=data.get('photo','')
            return post_creation(post_id,title,description,location,email,photo,short_description,time)
        except Exception as e:
            return JsonResponse({'status':'error','message':str(e)},status=400)
    else:
        return JsonResponse({'status':'error','message':'Invalid request method'},status=405)