import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, payload=None, api_key=None):
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=payload, auth=HTTPBasicAuth('apikey', api_key))
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=payload, auth=HTTPBasicAuth('apikey', api_key))
            status_code = response.status_code
            print("With status {} ".format(status_code))
            json_data = json.loads(response.text)
            return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


def post_request(url, json_payload):
    try:
        # Call post method of requests library with URL and parameters
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")

def get_dealers_from_cf(url, payload=None):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, payload)
    if json_result:
        # Get the row list in JSON as dealers
        if payload == None:
            dealers = json_result["rows"]
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
        else:
            dealers = json_result
            for dealer in dealers:
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],short_name=dealer["short_name"],
                st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
                results.append(dealer_obj)
        # For each dealer object

    return results

def get_reviews_from_cf(url, payload=None):
    results = []
    json_result = get_request(url, payload)
    if json_result:
        # Get the row list in JSON as dealers
        if payload == None:
            reviews = json_result["rows"]
            for review in reviews:
                review_doc = review["doc"]
                sentiment = analyze_review_sentiments(review_doc["review"])
                try:
                    review_obj = DealerReview(car_make=review_doc["car_make"], car_model=review_doc["car_model"],
                                        car_year=review_doc["car_year"], dealership=review_doc["dealership"], name=review_doc["name"],
                                        purchase=review_doc["purchase"], purchase_date=review_doc["purchase_date"], review=review_doc["review"], sentiment=sentiment)
                    results.append(review_obj)
                except KeyError:
                    pass
        else:
            reviews = json_result
            for review in reviews:
                sentiment = analyze_review_sentiments(review["review"])
                dealer_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], dealership=review["dealership"], name=review["name"],
                                    purchase=review["purchase"], purchase_date=review["purchase_date"], review=review["review"], sentiment=sentiment)
                results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, dealerID):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerID)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def analyze_review_sentiments(dealerreview):
    url = "https://us-east.functions.appdomain.cloud/api/v1/web/372df87c-dfe3-4ca8-b3fc-643d093167ce/dealership-package/get-sentiment"
    params = {}
    params["text"] = dealerreview
    json_result = get_request(url, params)
    return json_result["label"]

def post_review(url, json_payload):
    result = post_request(url, json_payload)
    return result



