import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if api_key != None:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
        return {}
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url=url, params=kwargs, json=json_payload)
    except:
        print("Network Exception Occurred")
        return {}
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["_id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"],dealer_id=dealer_doc["id"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url,id=dealerId)

    if json_result:
        dealer = json_result[0]
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["_id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"],dealer_id=dealer["id"])
        return dealer_obj

def get_dealers_by_state_from_cf(url, dealerState):
    result = get_request(url, states=dealerState)
    listResult = []

    if result:
        for dealer in result:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["_id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"],dealer_id=dealer["id"])
            listResult.append(dealer_obj)

        return listResult    


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    reviews = get_request(url, dealership = dealerId)
    reviews_list = []
    if reviews:
        for x in reviews:

            review_obj = DealerReview(dealership = x['dealership'], name = x['name'], review = x['review'], purchase=x['purchase'], id = x['id'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            if review_obj.purchase == True:
                review_obj.purchase_date = x['purchase_date']
                review_obj.car_make = x['car_make']
                review_obj.car_model = x['car_model']
                review_obj.car_year = x['car_year']
            reviews_list.append(review_obj)
        return reviews_list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    NLU_url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/9f8cc0ba-2263-42f9-ab11-d3588755545f/v1/analyze?version=2019-07-12"
    api_key = "venuSe6smIHzzbuD2ZH82Al66pessXEDcTB3FZM9j2L_"
    response = get_request(url=NLU_url, api_key=api_key, text=text, features='sentiment', return_analyzed_text=True)

    return response['sentiment']['document']['label']

