from django.urls import path
from .views import db_test

urlpatterns = [
    path('db-test/', db_test),
]
