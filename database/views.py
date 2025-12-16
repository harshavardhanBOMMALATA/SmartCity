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
    content=Posts.objects.all().values()
    content=list(content)
    return JsonResponse({'content':content},safe=False)