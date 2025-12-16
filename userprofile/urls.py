from django.urls import path
from . import views
from . import profile_api as api

app_name = 'userprofile'
urlpatterns = [
    path('', views.profie_view, name='profile'),
    path('api/profile_data/', api.profile_data, name='profile_data'),
    path('api/update_profile/', api.update_profile, name='update_profile'),
]