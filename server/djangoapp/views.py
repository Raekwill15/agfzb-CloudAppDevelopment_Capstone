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
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf

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
    # print(request.POST['username'])
    # print(request.POST['psw'])
    # print("_________________________________________________")
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
            print("______________________")
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
    if request.method == "GET":
        url = "https://raekwill15-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealer_by_id(request,id):
    dealer_id = id
    if request.method == "GET":
        url = f"https://raekwill15-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?id={dealer_id}"
        dealership = get_dealer_by_id_from_cf(url,dealer_id)
        return HttpResponse(dealership)

def get_dealers_by_state(request, state):
    print("We STARTED THE STATE URL!!!!!_________________")
    dealerState = state
    if request.method == "GET":
        url = f"https://raekwill15-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?state={state}"
        dealerships = get_dealers_by_state_from_cf(url, dealerState)
        return HttpResponse(dealerships)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    print("___________WE STARTED THE REVIEW URL!!!!__________")
    if request.method == "GET":
        url = f"https://raekwill15-3100.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get?id={id}"
        reviews = get_dealer_reviews_from_cf(url, id)
        return HttpResponse(reviews)




# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

