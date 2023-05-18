from django.urls import path
from .views import *
#from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('home/', home, name='home_web_base'),
    path('seller_form/', seller_form, name='seller_form'),
    path('login', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('register', register, name='register'),

    # path('pim/', get_data, name='home'),
    # path('webhook/', get_response_typeform, name='he'),
    # path('get/<int:pk>/', DetailMepView.as_view()),
    # path('update/<int:pk>/', UpdateMep.as_view()),
    # path('create/', CreateMep.as_view()),
    # path('delete/<int:pk>/', DeleteMep.as_view()),
    # path('login/', SignInView.as_view()),
    # path('logout/', SignOutView.as_view()),
    #path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]