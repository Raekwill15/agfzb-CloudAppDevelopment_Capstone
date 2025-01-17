from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here. 123


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, "djangoapp/about.html")

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    print(request.method)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')
    
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        username = request.POST['username']
        new_user=True
        try:
            User.objects.get(username=username)
            new_user=False
        except:
            logger.debug("{} is new user".format(username))
        if new_user:
            fname = request.POST['fname']
            lname = request.POST['lname']
            pswd = request.POST['pswd']
            user = User.objects.create_user(username=username,first_name=fname,last_name=lname,password=pswd)
            login(request,user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
        # username = request.POST['username']

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    context = {}

    if request.method == "GET":
        url = "https://raekwill15-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context['dealerships'] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Method when given a dealer id(int) will find the dealership that matches the given id in the API
def get_dealer_by_id(request,id):
    dealer_id = id
    if request.method == "GET":
        url = f"https://raekwill15-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(url,dealer_id)
        return HttpResponse(dealership)

# Method when given a state will find all dealers in the API that are located in the given state
def get_dealers_by_state(request, state):
    dealerState = state
    if request.method == "GET":
        url = f"https://raekwill15-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?state={state}"
        dealerships = get_dealers_by_state_from_cf(url, dealerState)
        return HttpResponse(dealerships)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# Method parameter id is used asa parameter for another method 
# to get all reviews from the dealership with the given id
# ...
def get_dealer_details(request, id):
    print("___________WE STARTED THE REVIEW URL!!!!__________")
    if request.method == "GET":
        context = {}
        url = f"https://raekwill15-3100.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get?id={id}"
        reviews = get_dealer_reviews_from_cf(url, id)
        url2 = f"https://raekwill15-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={id}"
        dealership = get_dealer_by_id_from_cf(url2, id)
        context['reviews'] = reviews
        context['dealership'] = dealership
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request,dealer_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            url = "https://raekwill15-3100.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/review/add?dealer_id={dealer_id}"
            review = {}
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            if request.POST['purchasecheck'] == 'on':
                review['purchase'] = True
            else:
                review['purchase'] = False
            review["name"] = "Anonymous"
            carinfo = request.POST['car'].split("-")

            review["car_model"] = carinfo[0]
            review["car_make"] = carinfo[1]
            review["car_year"] = carinfo[2]
            if review["purchase"] == True:
                review["purchase_date"] = datetime.utcnow().isoformat()
            
            review["id"] = 13
            json_payload = {}
            json_payload['review'] = review
            response = post_request(url, json_payload, dealer_id=dealer_id)
            return redirect("djangoapp:dealerbyid", id=dealer_id)
    elif request.method == "GET":
        context = {}
        cars = CarModel.objects.filter(dealer_id = dealer_id)
        url = f"https://raekwill15-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(url, dealer_id)
        context['cars'] = cars
        context['dealer_id'] = dealer_id
        context['dealership'] = dealership
        return render (request, 'djangoapp/add_review.html', context)
