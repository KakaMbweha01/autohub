#handle displaying the form and saving the submitted data
from django.shortcuts import render, redirect
from .forms import CarForm

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') # Redirect to homepage
        else:
            form = CarForm()
        return render(request, 'inventory/add_car.html', {'form': form})

#view will display a list of cars on the homepage
from django.shortcuts import render
from .models import Car

def index(request):
    cars = Car.objects.all() # retrieve all cars from the database
    return render(request, 'inventory/car_detail.html', {'cars': cars})
def car_detail(request, id):
    car = Car.objects.get(id=id) #retrieve the car by its ID
    return render(request, 'inventory/car_detail.html', {'car': car})

# Update the Homepage View to Handle Search Queries
from django.db.models import Q # import Q for complex lookups

def index(request):
    query = request.GET.get('q') # Get the search query from the request
    if query:
        cars = Car.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    else:
        cars = Car.objects.all() # show all cars if no search query
    return render(request, 'inventory/index.html', {'cars': cars, 'query': query})