from django.urls import path
from .views import *
#from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('home/', home, name='home_web_base'),
    path('dashboard/', seller_form, name='dashboard'),
    path('login', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('dashboard/<str:id>/', dashboard_detail),
    path('register', register, name='register'),
]