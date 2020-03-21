from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('branch',views.branch,name='branch'),
    path('account',views.account,name='account'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('send_money',views.send_money,name='send_money'),
    path('recive_money',views.recive_money,name='recive_money'),
    path('add_branch',views.add_branch,name='add_branch'),
]
