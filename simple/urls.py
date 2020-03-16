from django.urls import path
from . import views

app_name = 'simple'

urlpatterns = [
    path('loginsuccess/', views.login_success, name='loginsucess'),
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('userlocked/', views.userlocked, name='userlocked'),

]
