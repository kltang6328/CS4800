import json
import boto3
import requests
  
def get_api_key():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:891321150257:function:yelp_get_api_key',
            InvocationType = 'RequestResponse'
        )
    yelp_api_key = json.load(response['Payload'])['body']['api_key']
    return yelp_api_key

yelp_key = get_api_key()
print(yelp_key)

def lambda_handler(event, context):
    if event["request_type"] == "search":
        return search_handler(event)
    elif event["request_type"] == "fetch_from_id":
        return fetch_from_id_handler(event)
    return {
        'statusCode':404
    }
    
def search_handler(event):
    url = "https://api.yelp.com/v3/businesses/search"
    location = event["location"]
    terms = event["terms"]
    
    payload = {
        "location" : location,
        "sort_by":"best_match",
        "limit" : 3,
        "term" : terms
    }
    headers = {
        "accept": "application/json",
        "Authorization": ("Bearer " + yelp_key)
    }
    response = requests.get(url,params=payload, headers=headers)
    print(json.loads(response.text))
    print(json.loads(response.text)["businesses"])
    return {
        'statusCode':200,
        'body': {
            'response' : json.loads(response.text)["businesses"]
        }
    }
def fetch_from_id_handler(event):
    url = "https://api.yelp.com/v3/businesses/"
    id = event["id"]
    
    headers = {
        "accept": "application/json",
        "Authorization": ("Bearer " + yelp_key)
    }
    
    response = requests.get(url + id, headers=headers)
    print(json.loads(response.text))
    return {
        'statusCode':200,
        "headers" : {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
        },
        'body': {
            'response' : json.loads(response.text)
        }
    }