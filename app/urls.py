from django.urls import path,include
from rest_framework.authtoken import views
from .views import *
urlpatterns = [
    path('',AuthenticateUser.as_view(),name='auth'),
    path('get-token/',views.obtain_auth_token),
    path('signup/',CreateUser.as_view(),name='register'),
    path('login/',Login.as_view()),
    path('logout/',Logout.as_view()),
    path('get-user/',GetUser.as_view()),
    path('profile/',GetProfile.as_view()),
    path('investment/',CreateInvestment.as_view()),
    path('change-password/',ChangePassword.as_view()),
    path('get-agreement/<int:pk>',handleAgreement.as_view()),
    path('withdraw/',Withdraw.as_view())
]
