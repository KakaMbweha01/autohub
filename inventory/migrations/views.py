from django.shortcuts import render
from .models import Car

def index(request):
    cars = Car.objects.all() # retrieve all cars from the database
    return render(request, 'inventory/car_detail.html', {'cars': cars})
def car_detail(request, id):
    car = Car.objects.get(id=id) #retrieve the car by its ID
    return render(request, 'inventory/car_detail.html', {'car': car})