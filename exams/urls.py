from django.urls import path

from . import views

urlpatterns = [
    path('', views.azmoon, name='azmoon'),
    path('message/', views.message, name='message'),
]
