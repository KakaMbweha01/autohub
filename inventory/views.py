# Active: 1733979292823@@127.0.0.1@3306@autohub
from django.shortcuts import render, redirect,  get_object_or_404
from inventory.forms import CarForm, UserRegistrationForm, UserProfileForm, ContactForm, ReviewForm
from inventory.models import Car, Review
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
from django.core.mail import send_mail

# Create your views here.
@login_required
def profile(request):
    user = request.User
    return render(request, 'inventory/profile.html', {'user': user})

@login_required
def car_list(request):
    query = request.GET.get('q', '')
    cars = Car.objects.all().order_by('name')
    if query:
        cars = Car.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(year__icontains=query)
            ).order_by('year')
    else:
        cars = Car.objects.all().order_by('year')

    cars = Car.objects.annotate(average_rating=Avg('reviews')) # Annotate average rating
    # Filtering
    brand = request.GET.get('brand')
    name = request.GET.get('name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if name:
        cars = cars.filter(name__icontains=name)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)
    if min_year:
        cars = cars.filter(year__gte=min_year)
    if max_year:
        cars = cars.filter(year__lte=max_year)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by in ['price', '-price', 'year', '-year', 'average_rating', '-average_rating']:
        cars = cars.order_by(sort_by)

    paginator = Paginator(cars, 5) # Display 5 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/index.html', {'cars': cars, 'page_obj': page_obj, 'query': query, 'query_params': request.GET})
    #return render(request, 'inventory/index.html', {'cars': cars, 'query': query})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = ReviewForm()
    return render(request, 'inventory/car_detail.html', {
        'car': car,
        'reviews': reviews,
        'form': form
    })

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

def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
        else:
            # if form is invalid re-render form with errors
            return render(request, 'inventory/edit_car.html', {'form': form, 'car': car})
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

@login_required
def user_dashboard(request):
    # get cars added by currently logged-in user
    user = request.user # Retrieves loged-in user
    user_cars = Car.objects.filter(added_by=request.user)
    return render(request, 'inventory/user_dashboard.html', {'user': user, 'user_cars': user_cars})

@login_required
def view_profile(request):
    return render(request, 'inventory/view_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.User.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.sucsess(request, 'Your Profile has been updated successfully')
            return redirect('view_profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)


    return render(request, 'inventory/edit_profile.html', {'user_form': user_form, 'profile_form':profile_form})

def compare_cars(request):
    car_ids = request.GET.getlist('cars') # Get selected car IDs
    cars = Car.objects.filter(id__in=car_ids)

    return render(request, 'inventory/compare.html', {'cars': cars})

@login_required
def toggle_favorite(request, car_id):
    user_profile = request.user.userprofile
    car = get_object_or_404(Car, id=car_id)

    if car in user_profile.favorites.all():
        user_profile.favorites.remove(car) # Remove from favorites
        favorited = False
    else:
        user_profile.favorites.add(car) # Add to favorites
        favorited = True

    return JsonResponse({'favorited': favorited})

@login_required
def favorites_list(request):
    user_profile = request.user.userprofile
    favorites = user_profile.favorites.all()
    return render(request, 'inventory/favorites.html', {'favorites': favorites})

# A view for the contact page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # send email
            send_mail(
                f"New Inquiry from {name}",
                message,
                email,
                ['admin@example.com'], # Replace with your admin email
                fail_Silently=False,
            )

            return render(request, 'inventory/contact_success.html', {'name': name})
        else:
            form=ContactForm()

        return render(request, 'inventory/contact.html', {'form': form})

# the home view
def home(request):
    return render(request, 'inventory/home.html') # hapa bado kazi iko bwana

def search_cars(request):
    query = request.GET.get('q', '')
    cars = Car.objects.filter(name__icontains=query) if query else Car.objects.all()
    return render(request, 'inventory/search_results.html', {'cars': cars, 'query': query})