from django.shortcuts import render, redirect,  get_object_or_404
from inventory.forms import CarForm, UserRegistrationForm
from inventory.models import Car
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
@login_required
def profile(request):
    user = request.user
    return render(request, 'inventory/profile.html', {'user': user})

@login_required
def car_list(request):
    query = request.GET.get('q', '')
    cars = Car.objects.all()
    if query:
        cars = Car.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query) | Q(year__icontains=query))
    else:
        cars = Car.objects.all()
    paginator = Paginator(cars, 5) # Display 5 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/index.html', {'page_obj': page_obj, 'query': query})
    #return render(request, 'inventory/index.html', {'cars': cars, 'query': query})

def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    return render(request, 'inventory/car_detail.html', {'car': car})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'inventory/add_car.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('car_list')
        else:
            form = AuthenticationForm()
        return render(request, 'inventory/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('car_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user) # login the user after registration
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'inventory/register.html', {'form': form})

def edit_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
        else:
            form = CarForm(instance=car)
        return render(request, 'inventory/edit_car.html', {'form': form, 'car': car})

@login_required
def delete_car(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'inventory/delete_car.html', {'car': car})