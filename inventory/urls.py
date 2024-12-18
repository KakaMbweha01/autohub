from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.car_list, name='car_list'), # Homepage
    path('car<int:id>/', views.car_detail, name='car_detail'), # cardetails
    path('add/', views.add_car, name='add_car'), # add a car
    path('edit/<int:id>/', views.edit_car, name='edit_car'), # car edit
    path('delete/<int:id>/', views.delete_car, name='delete_car'), # delete car
    path('profile/', views.view_profile, name='view_profile'), # profile
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'), # login
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # logout
    path('register/', views.register, name='register'), # registration
    path('', views.home, name='home'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'), # dashboard
    path('profile/edit/', views.edit_profile, name='edit_profile'), # edit profile
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='inventory/change_password.html'), name='change_password'), # change password
    path('profile/change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='inventory/change_password_done.html'), name='password_change_done'), # change password done
    path('compare/', views.compare_cars, name='compare_cars'),
    path('toggle-favorite/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'), # toggling favorites
    path('favorites/', views.favorites_list, name='favorites_list'), # view favorites list
    path('contact/', views.contact, name='contact'), # view contacts
]
