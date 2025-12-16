from django.urls import path
from . import views
app_name='postings'
urlpatterns = [
    path('', views.new_post, name='postings_home'),
]