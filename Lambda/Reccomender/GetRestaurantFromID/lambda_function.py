import json
import random
import boto3
import os

print('Loading function')

def lambda_handler(event, context):
    print("BEGIN LOG HERE")
    print(event)
    # data = body["restaurants"]
    # for restaurant in data:
    #     print("value1 = " + restaurant['name'])
    #     print("value2 = " + restaurant['rating'])
    bodystring = event["body"]
    body = json.loads(bodystring)
    id = body["id"]
    
    yelp_payload = {
        "request_type" : "fetch_from_id",
        "id" : id
    }
        
    if os.path.isfile("/tmp/restaurants.json"):
        print("USING CACHED FILE")
        foundInFile = False
        with open("/tmp/restaurants.json", "r") as infile:
            json_object = json.load(infile)
            print(id)
            print(json_object)
            if id in json_object:
                print("FOUND CACHED")
                foundInFile = True
                yelp_response = json_object[id]
        if not foundInFile:
            print("NOT FOUND IN CACHED")
            
            yelp_response = get_yelp_response(yelp_payload)
                
            with open("/tmp/restaurants.json", "w") as outfile:
                json_object[id] = yelp_response
                json_string = json.dumps(json_object)
                outfile.write(json_string)
            
    else:
        print("CACHE NOT FOUND")
        
        yelp_response = get_yelp_response(yelp_payload)
        print("yelp_response")
        print(yelp_response)
        entry = {id : yelp_response}
        newDict = entry
        
        json_string = json.dumps(newDict)
        
        with open("/tmp/restaurants.json", "x") as outfile:
            outfile.write(json_string)

    restaurant_tags = []
    restaurant_categories = []
    address = ""
    for value in yelp_response["categories"]:
        restaurant_tags.append(value["title"])
        restaurant_categories.append(value["alias"])
    
    first_address = True
    for value in yelp_response["location"]["display_address"]:
        if not first_address:
            address += ", "
        address += value
        first_address = False
    
    
    print(json.dumps(yelp_response))
    
    result = {
        "name" : yelp_response["name"] if "name" in yelp_response else "N/A",
        "id" : yelp_response["id"] if "id" in yelp_response else "N/A",
        "url" : yelp_response["url"] if "url" in yelp_response else "N/A",
        "image_url" : yelp_response["image_url"] if "image_url" in yelp_response else "N/A",
        "location" : address if ("location" in yelp_response) else "N/A",
        "restaurant_types" : restaurant_tags,
        "restaurant_categories" : restaurant_categories,
        "rating" : yelp_response["rating"] if "rating" in yelp_response else "N/A",
        "price" : yelp_response["price"] if "price" in yelp_response else "N/A",
        "phone" : yelp_response["display_phone"] if "display_phone" in yelp_response else "N/A"
    }
    
    # response = {
    #     "statusCode" : 200,
    #     "headers" : {
    #         "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
    #     },
    #     "body" : result
    # }
    response = result;
    
    
    return response
    #raise Exception('Something went wrong')

def get_yelp_response(message):
    print("IM DOING YELP STUFF NOW")
    lambda_client = boto3.client('lambda')
    request = message
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:891321150257:function:yelp_invoke_api',
            InvocationType = 'RequestResponse',
            Payload=json.dumps(request).encode()
        )
    print(response['Payload'])
    recommendation = json.load(response['Payload'])['body']['response']
    return recommendation