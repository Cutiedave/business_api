from django.urls import path
from .views import *
#from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('home/', home, name='home_web_base'),
    path('dashboard/', seller_form, name='dashboard'),
    path('login', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('dashboard/<str:email>/', dashboard_detail),
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