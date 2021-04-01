from django.urls import path
from . import views

urlpatterns=[
     path('register',views.register,name="sign-up"),
     path("login", views.login_request, name="login"),
     path("logout", views.logout_request, name= "logout"),
     path('index',views.index,name='index'),
     path('',views.index,name='index')


]