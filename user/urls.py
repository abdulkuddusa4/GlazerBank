from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.Registration.as_view(), name='user-registration'),
    path('profile-create/', views.CreateProfile.as_view(), name='user-profile-create'),
    path('user-profile/', views.UserProfile.as_view(), name='user-profile'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
]