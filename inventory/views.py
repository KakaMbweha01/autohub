# Active: 1733979292823@@127.0.0.1@3306@autohub
from django.shortcuts import render, redirect,  get_object_or_404, get_list_or_404
from .forms import CarForm, UserRegistrationForm, UserProfileForm, ContactForm, ReviewForm
from .models import Car, Review, UserProfile, Notification
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
from django.core.mail import send_mail
#from django.db.models.signals import post_save
#from django.dispatch import receiver
import logging
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from .serializers import CarSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


# Create your views here.
@login_required
def profile(request):
    user = request.User
    return render(request, 'inventory/profile.html', {'user': user})

# view for the list of cars
@login_required
def car_list(request):
    query = request.GET.get('q', '')
    unread_notifications = request.user.notifications.filter(is_read=False).all()
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

    cars = Car.objects.all().order_by('name')

    paginator = Paginator(cars, 5) # Display 5 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/index.html', {
        'cars': cars,
        'page_obj': page_obj,
        'query': query,
        'query_params': request.GET,
        'unread_notifications': unread_notifications})
    #return render(request, 'inventory/index.html', {'cars': cars, 'query': query})

# view for the details of the car
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    # calculate average rating
    average_rating = car.reviews.aggregate(Avg('rating'))['rating__avg']
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
    context = {
        'car': car,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating or "No ratings yet", # default message if no ratings exist
    }
    return render(request, 'inventory/car_detail.html', context)

# view to add a car
def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            # car creation logic
            car = Car.objects.create(
                name=request.POST['name'],
                brand=request.POST['brand'],
                year=request.POST['year'],
                price=request.POST['price'],
                added_by=request.user,
            )
            #car.added_by = request.user
            car.save()
            #  notfications for all the users about the new car
            users = User.objects.exclude(id=request.user.id) # exclude user who addded car
            notification_message = f"A new car '{car.name}' has been added by {request.user.username}."
            notifications = [
                Notification(user=user, message=notification_message)
                for user in users
            ]
            Notification.objects.bulk_create(notifications) # batch creation
            messages.success(request, "Car added successfully!")
            return redirect('car_list')
        else:
            messages.error(request, "There was an error adding the car. Please check the form.")
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

# compare cars
def compare_cars(request):
    car_ids = request.GET.getlist('cars') # Get selected car IDs
    #cars = get_list_or_404(Car, id__in=car_ids)
    #Fetch selected cars
    cars = Car.objects.filter(id__in=car_ids)
    if not cars.exists():
        return render(request, 'inventory/compare.html', {'error': 'No cars selected for comparson.'})

    return render(request, 'inventory/compare.html', {'cars': cars})

# add a car to favorites
logger = logging.getLogger(__name__)
@transaction.atomic
@login_required
def add_to_favorites(request, car_id):
    # debug to verify request.user.id is not None
    logger.debug(f"User: {request.user}, User ID: {request.user.id}")
    # check authentication status
    if not request.user.is_authenticated:
        return redirect('login')
    # get car object
    car = get_object_or_404(Car, id=car_id)
    # ensure the user has a userprofile
    #created = UserProfile.objects.get_or_create(user=request.user)
    user_profile = request.user.userprofile
    if car not in user_profile.favorite_cars.all():
        # Add the car to user's favorite
        user_profile.favorite_cars.add(car)
        messages.success(request, f"{car.name} has been added to your favorites!")
         # notifying the car owner when someone has added their car to favorites
        #Notification.objects.create(
            #user = car.added_by,
            #message = f"{request.userprofile} has favorited your car '{car.name}'."
            # )
    else:
        messages.info(request, f"{car.name} is already in your favorites.")
    return redirect('favorites')

# remove a car from favorites
@login_required
def remove_from_favorites(request, car_id):
    # get the car object
    car = get_object_or_404(Car, id=car_id)
    #ensure the user has a profile
    #created = UserProfile.objects.get_or_create(user=request.user)
    user = request.user
    user_profile = user.userprofile
    if car in user_profile.favorite_cars.all():
        # remove car from user's favorite
        user_profile.favorite_cars.remove(car)
        messages.success(request, f"{car.name} has been removed from your favorites!")
    else:
        messages.warning(request, f"{car.name} is not in your favorites.")
    return redirect('favorites')

# favorite cars list
@login_required
def favorites_cars(request):
    user = request.user
    try:
        user_profile = user.userprofile
        favorite_cars = user_profile.favorite_cars.all()
    except UserProfile.DoesNotExist:
        # Handle the case where the profile does not exist
        return render(request, 'inventory/error.html', {'message': 'User profile not found'})

    #favorite_cars = user_profile.favorite_cars.all()
    return render(request, 'inventory/favorites.html', {'favorite_cars': favorite_cars})

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

# car search view
def search_cars(request):
    query = request.GET.get('q', '') # search term
    #cars = Car.objects.all()
    min_price = request.GET.get('min_price', None) # minimum price filter
    max_price = request.GET.get('max_price', None) # maximum price filter
    year = request.GET.get('year', None) # Year filter
    sort_by = request.GET.get('sort_by', 'price_asc') # sort by attribute, default to 'price_asc'
    #brand = request.GET.get('brand') # get the brand name
    results = Car.objects.all()
    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    if min_price:
        results = results.filter(price__gte=min_price)

    if max_price:
        results = results.filter(price__lte=max_price)

    if year:
        results = results.filter(year=year)

    # sorting
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')
    elif sort_by == 'year_desc':
        results = results.order_by('-year')

    # pagination of results
    paginator = Paginator(results, 4) # 4 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'query': query,
               'results': results,
               'min_price': min_price,
               'max_price': max_price,
               'year': year,
               'sort_by': sort_by,
               'page_obj': page_obj,
    }
    return render(request, 'inventory/search_results.html', context)

# adding a car to the wish list
@login_required
def add_to_wishlist(request, id):
    car = get_object_or_404(Car, id=id)
    if request.user not in car.favorited_by.all():
        car.favorited_by.add(request.user)
    return redirect('car_detail', id=id)

# removing a car from the wish list
@login_required
def remove_from_wishlist(request, id):
    car = get_object_or_404(Car, id=id)
    if request.user in car.favorited_by.all():
        car.favorited_by.remove(request.user)
    return redirect('wishlist')

# the wishlist view
def wishlist(request):
    wishlist_cars = request.user.wishlist.all()
    return render(request, 'inventory/wishlist.html', {'wishlist_cars': wishlist_cars})

# review
@login_required
def add_review(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('car_detail', id=car.id)
        else:
            form = ReviewForm()
        return render(request, 'inventory/add_review.html', {'form': form, 'car': car})

# submitting a review & Adding a message
@login_required
def submit_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
        else:
            messages.error(request, "There was an error submitting your review. Please try again.")
    return redirect('car_detail', car_id=car.id)

# list user notifications
@login_required
def notifications(request):
    user_notifications = request.user.notifications.all()
    return render(request, 'inventory/notifications.html', {'notifications': user_notifications})

# mark notification as read
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    #request.user.notifications.update(is_read=True)
    #messages.info(request, "All notifications marked as read")
    return redirect('user_dashboard')

# mark all notifications as read
@login_required
def mark_all_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.info(request, "All notifications marked as read.")
    return redirect('home')

# Api view for car list
class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'price'] # apa eka fields to filter by
    search_fields = ['name'] # allow search on the name of a car
    ordering_fields = ['year', 'price'] # allow sorting
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

# Api view for car detail
class CarDetailAPIView(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
            serializer = CarSerializer(car)
            return Response(serializer.data)
        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

# api view for adding a car
class AddCarAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

# api view to add a review
class AddReviewAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

# api view for car reviews
class CarReviewsAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        car_id  = self.kwargs['car_id']
        return Review.objects.filter(car_id=car_id)

# api view to delete a car
''' class DeleteCarAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated] '''