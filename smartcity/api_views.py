from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from database.views import check_user_credentials,register_user



@csrf_exempt
def login_api(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            email=data.get('email')
            password=data.get('password')
            if(check_user_credentials(email,password)):
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
