from django.urls import path, include
from User import views

urlpatterns = [
    path('account/login', views.LoginView.as_view(), name='login'),
    path('account/new/signup', views.SignUp.as_view(), name='register'),
]