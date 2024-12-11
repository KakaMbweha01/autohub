from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('car-list/', views.car_list, name='car_list'), # Homepage
    path('<int:id>/', views.car_detail, name='car_detail'), # cardetails
    path('add/', views.add_car, name='add_car'), # add a car
    path('edit/<int:id>/', views.edit_car, name='edit_car'), # car edit
    path('delete/<int:id>/', views.delete_car, name='delete_car'), # delete car
    path('profile/', views.profile, name='profile'), # profile
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'), # login
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # logout
    path('register/', views.register, name='register'), # registration
    path('', views.home, name='home'), 
]
