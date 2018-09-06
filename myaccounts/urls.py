from django.urls import path
from . import views

app_name = 'myaccounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration_view, name='signup'),
]
