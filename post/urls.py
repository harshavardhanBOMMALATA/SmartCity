from django.urls import path
from . import views 

app_name = 'post'

urlpatterns = [
    path('', views.post, name='post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('api/<int:postId>/',views.getpost,name='getpost'),
    path('poll/agree/<int:postid>/',views.agree,name='agree'),
    path('poll/disagree/<int:postid>/',views.disagree,name='agree'),
    path('poll/result/<int:postid>/',views.result,name="result"),
    path('poll/response/<int:postId>/',views.response,name="response"),
    path('verdict/<int:postid>/',views.verdict,name="verdict"),
    path('myposts/',views.myposts,name='myposts'),
    path('all-myposts/',views.all_myposts,name="all_myposts"),
    path('poll/loginornot/',views.loginornot,name="loginornot"),
    path('poll/responseverdict/<int:postId>',views.responseverdict,name="responseverdict"),
]