from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from database.views import user_details,update_user_profile
import json

def is_user(request):
    return request.session.get('email') is not None

@csrf_exempt
def profile_data(request):
    email = request.session.get('email')

    if not email:
        return JsonResponse(
            {'status': 'login', 'message': 'User not logged in'},
            status=401
        )

    try:
        return user_details(email)
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)},
            status=400
        )

@csrf_exempt
def update_profile(request):
    if request.method=='POST':
        if is_user(request) is False:
            return JsonResponse({'status':'login','message':'User not logged in'},status=401)
        try:
            data=json.loads(request.body)
            email=request.session.get('email')
            name=data.get('name')
            phonenumber=data.get('phonenumber','')
            address=data.get('address','') 
            return update_user_profile(email,name,phonenumber,address)
        except Exception as e:
            return JsonResponse({'status':'error','message':str(e)},status=400) 