from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarDealer, DealerReview, CarModel
from django.utils import timezone
from .forms import ReviewForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:about')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:about')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:about")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        dealerships = CarDealer.objects.all()
        context = {'dealership_list': dealerships}
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":  
        dealership = get_object_or_404(CarDealer, pk=dealer_id)
        reviews = DealerReview.objects.filter(dealership=dealer_id)
        context = {'dealership': dealership, 'reviews': reviews}
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
#      context = {}
#      return render(request, 'djangoapp/add_review.html', context)

def add_review(request, dealer_id):
    dealer = get_object_or_404(CarDealer, pk=dealer_id)

    if request.method == 'GET':
        # Query the cars with the dealer id to be reviewed
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {'dealer': dealer, 'cars': cars}
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
            form = ReviewForm(request.POST)
            print(form.cleaned_data['content'])
            # if form.is_valid():
            #     try:
            #         content = form.cleaned_data['content']
            #         purchasecheck = form.cleaned_data['purchase_check']
            #         car = form.cleaned_data['car']
            #         purchasedate = form.cleaned_data['purchase_date']
            #         sentiment = form.cleaned_data['sentiment']
            #         purchase_year = purchasedate.strftime("%Y")

            #         new_review = DealerReview(
            #         dealership=dealer,
            #         content=content,
            #         purchase_check=purchasecheck,
            #         car_make=car.car_make.name,
            #         car_model=car.name,
            #         car_year=car.year,
            #         purchase_year=purchase_year,
            #         review_time=timezone.datetime.utcnow().isoformat(),
            #         sentiment=sentiment
            #         )
            #         new_review.save()
            #     except Exception as e:
            #         print(f"An error occurred while saving the review: {e}")

    return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    

    # elif request.method == 'POST':
    #     form = ReviewForm(request.POST)
        
    #     if form.is_valid():
    #         # Get values from the valid form
    #         content = form.cleaned_data['content']
    #         purchasecheck = form.cleaned_data['purchase_check']
    #         car = form.cleaned_data['car']
    #         purchasedate = form.cleaned_data['purchase_date']
    #         sentiment = form.cleaned_data['sentiment']

    #         # Convert purchase date to year only
    #         purchase_year = purchasedate.strftime("%Y")

    #         # Create a new DealerReview object
    #         new_review = DealerReview(
    #             dealership=dealer,
    #             content=content,
    #             purchase_check=purchasecheck,
    #             car_make=car.car_make.name,
    #             car_model=car.name,
    #             car_year=car.year,
    #             purchase_year=purchase_year,
    #             review_time=timezone.datetime.utcnow().isoformat(),
    #             sentiment=sentiment
    #         )

    #         # Save the review to the database
    #         new_review.save()

    #         # Redirect user to the dealer details page
    #         return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    #     else:
    #         # Form is not valid, return a response indicating the error
    #         return render(request, 'djangoapp/add_review.html', {'dealer': dealer, 'form': form})

    
    # elif request.method == 'POST':
    #     form = ReviewForm(request.POST)
        
    #     if form.is_valid():
    #         # Get values from the valid form
    #         content = form.cleaned_data['content']
    #         purchasecheck = form.cleaned_data['purchase_check']
    #         car = form.cleaned_data['car']
    #         purchasedate = form.cleaned_data['purchase_date']
    #         sentiment = form.cleaned_data['sentiment']

    #         # Convert purchase date to year only
    #         purchase_year = purchasedate.strftime("%Y")

    #         # Create a new DealerReview object
    #         new_review = DealerReview(
    #             dealership=dealer,
    #             content=content,
    #             purchase_check=purchasecheck,
    #             car_make=car.car_make.name,
    #             car_model=car.name,
    #             car_year=car.year,
    #             purchase_year=purchase_year,
    #             review_time=timezone.datetime.utcnow().isoformat(),
    #             sentiment=sentiment
    #         )

    #         # Save the review to the database
    #         new_review.save()

    #         # Redirect user to the dealer details page
    #         return redirect('djangoapp:dealer_details', dealer_id=dealer_id)

    # elif request.method == 'POST':
    #     # Get values from the review form
    #     content = request.POST.get('content')
    #     purchasecheck = request.POST.get('purchasecheck', False)
    #     car_id = request.POST.get('car')
    #     purchasedate = request.POST.get('purchasedate')

    #     # Convert purchase date to year only
    #     purchase_year = timezone.datetime.strptime(purchasedate, "%m/%d/%Y").strftime("%Y")

    #     # Create a new DealerReview object
    #     new_review = DealerReview(
    #         dealership=dealer,
    #         content=content,
    #         purchase_check=purchasecheck,
    #         car=CarModel.objects.get(pk=car_id),
    #         purchase_year=purchase_year,
    #         review_time=timezone.datetime.utcnow().isoformat()
    #     )

    #     # Save the review to the database
    #     new_review.save()

    #     # Redirect user to the dealer details page
    #     return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
