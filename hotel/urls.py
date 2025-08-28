from django.urls import path
from hotel import views

urlpatterns = [
    path('', views.home, name='home'),
]