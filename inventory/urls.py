from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #Home page view
    path('car/<int:id>/', views.car_detail, name='car_detail') # detail view
    path('add-car/', views.add_car, name='add_car') #Add this line
    ]