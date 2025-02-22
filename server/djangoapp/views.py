from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_reviews_from_cf, post_review
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html') 

def add_review_page(request, dealer_id):
    context = {}
    car_models = CarModel.objects.filter(dealer_id=dealer_id)
    dealer = get_dealer_details(request, dealer_id)
    context['cars'] = car_models
    context['dealer_id'] = dealer_id
    # print(dealer)
    return render(request, 'djangoapp/add_review.html', context) 
# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html') 

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        context['dealers'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/dealership"
        # Get dealers from the URL
        payload = {'dealerID': dealer_id}
        dealerships = get_dealers_from_cf(url, payload)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer. for dealer in dealerships])
        # Return a list of dealer short name
        context['dealers'] = dealerships
        return dealerships[0]
        # return render(request, 'djangoapp/dealer_detail.html', context)

def get_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/review"
        # Get dealers from the URL
        payload = {'dealerID': dealer_id}
        dealer = get_dealer_details(request, dealer_id)
        reviews = get_reviews_from_cf(url, payload)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer. for dealer in dealerships])
        # Return a list of dealer short name
        context['reviews'] = reviews
        context['dealer'] = dealer.full_name
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

def get_reviews(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/review"
        # Get dealers from the URL
        reviews = get_reviews_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer. for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(reviews)
        # return render(request, 'djangoapp/index.html', context)

def add_review(request):
    if request.method == "POST":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/review"
        dealership = request.POST['dealer_id']
        name = request.POST["name"]
        car_id = request.POST["car"]
        car = get_object_or_404(CarModel, pk=car_id)
        purchase = "false"
        if request.POST["purchasecheck"]:
            purchase = "true"
        purchase_date = request.POST["purchase_date"]
        review = request.POST["content"]
        payload = {
            "dealership": int(dealership.replace("/", "")), 
            "car_make": car.carmake.name, 
            "car_model": car.name,
            "car_year": car.year.strftime("%Y"),
            "name": name,
            "purchase": purchase, 
            "purchase_date": purchase_date,
            "review": review
        }
        response = post_review(url, payload)
        return HttpResponse(response)


