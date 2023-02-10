from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home-view'),
    path('about/', views.about, name='about-view'),
    path('services/', views.services, name='services-view'),
    path('contacts/', views.contacts, name='contact-view'),
]