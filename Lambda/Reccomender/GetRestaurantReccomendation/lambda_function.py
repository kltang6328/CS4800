import json
import random
import openai
import boto3

print('Loading function')

def lambda_handler(event, context):
    
    print("TEST LOG:")
    print(event)
    # data = body["restaurants"]
    # for restaurant in data:
    #     print("value1 = " + restaurant['name'])
    #     print("value2 = " + restaurant['rating'])
    
    bodystring = event["body"]
    body = json.loads(bodystring)
    print(body)
    location = body["location"]
    print(location)
    message = body["message"]
    print(message)
    
    terms = "food"
    categories = ""
    
    if(message != ""):
        terms = get_openai_response(message)
    
    liked_restaurants = body["liked_restaurants"]
    liked_dict = {}
    alias_dict = {}
    for liked_restaurant in liked_restaurants:
        resp = get_restaurant_response(liked_restaurant)
        print(resp)
        rest_types = resp["categories"]
        for t in rest_types:
            if(t in liked_dict):
                liked_dict[t] += 1
            else:
                liked_dict[t] = 1 
        rest_aliases = resp["aliases"]
        for a in rest_aliases:
            if(a in alias_dict):
                alias_dict[a] += 1
            else:
                alias_dict[a] = 1
    print(liked_dict)
    
    if(len(liked_dict) > 0):
        max_num = max(liked_dict.values())
        most_common = []
        cur_max = max_num
        while(len(most_common) < 3 and len(most_common) < len(liked_dict)):
            most_common =[k for k,v in liked_dict.items() if int(v) == cur_max]
            cur_max = cur_max - 1
        cat_sample = random.sample(most_common, 3)
        for cat in cat_sample:
            if(categories != ""):
                categories += ","
            categories += cat
    if(len(alias_dict) > 0):
        max_num = max(alias_dict.values())
        most_common = []
        cur_max = max_num
        while(len(most_common) < 3 and len(most_common) < len(liked_dict)):
            most_common =[k for k,v in alias_dict.items() if int(v) == cur_max]
            cur_max = cur_max - 1
            
        terms += "," + most_common[random.randint(0, len(most_common)-1)]
    print("terms")
    print(terms)
    print("categories")
    print(categories)
    
    yelp_payload = {
        "request_type" : "search",
        "location" : location,
        "terms" : terms
    }
    print(json.dumps(yelp_payload))
    
    yelp_response = get_yelp_response(yelp_payload)
    print(json.dumps(yelp_response))
    id_array = []
    for restaurant in yelp_response:
        id_array.append(restaurant["id"])
        
    result = id_array
        
    # dummy = [
    #         {"name" : "McDonalds", "address" : "14325 McNab Ave, Bellflower, CA 90706", "hours" : "24/7", "food_type" : "fast food", "average rating" : "3.5", "image" : "https://img-9gag-fun.9cache.com/photo/a3Q5VW5_460s.jpg"},
    #         {"name" : "Sublimotion", "address" : "14894 Leer Rd, Posen, MI 49776", "hours" : "1:00PM-2:00PM", "food_type" : "fine_dining", "average rating" : "1.2", "image" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2z2pvWMfAc0esndqPY4oU_al7ubp49weIyg&usqp=CAU"},
    #         {"name" : "Burger King", "address" : "2833 North Ave, Grand Junction, CO 81503", "hours" : "24/7", "food_type" : "fast food", "average rating" : "3", "image" : "https://thechive.com/wp-content/uploads/2019/12/person-hilariously-photoshops-animals-onto-random-things-xx-photos-25.jpg?attachment_cache_bust=3136487&quality=85&strip=info&w=400"},
    #         {"name" : "Pu Pu Hot Pot", "address" : "Silver Springs, NV 89429", "hours" : "8:00AM-10:00PM", "food_type" : "hot pot", "average rating" : "4.8", "image" : "https://i.seadn.io/gae/2hDpuTi-0AMKvoZJGd-yKWvK4tKdQr_kLIpB_qSeMau2TNGCNidAosMEvrEXFO9G6tmlFlPQplpwiqirgrIPWnCKMvElaYgI-HiVvXc?auto=format&dpr=1&w=1000"},
    #         {"name" : "Big Dong", "address" : "3801 W Temple Ave, Pomona, CA 91768", "hours" : "7:00AM-7:00PM", "food_type" : "asian fusion", "average rating" : "0", "image" : "https://collegevine.imgix.net/2a5d9bfd-8666-4cc5-98c5-e3daa75518dd.jpg"},
    #         {"name" : "Los Pollos Hermanos", "address" : "2031 Yosemite Blvd, Modesto, CA 95354", "hours" : "24/7", "food_type" : "chicken", "average rating" : "100", "image" : "https://lh5.googleusercontent.com/p/AF1QipN9EKKrohzOF655KPQE-R-ZeYqquI9LlrugH8m0=w408-h544-k-no"}
    #     ]
    # result = random.sample(dummy, 3)
    # result = get_openai_response(body["message"])
    # response = {
    #     "statusCode" : 200,
    #     "headers" : {
    #         "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    #         "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
    #         "Access-Control-Allow-Methods": "*"
    #     },
    #     "body" : {"restaurants" : result}
    # }
    
    response = result
    print(response)
    return response
    #raise Exception('Something went wrong')

def get_openai_response(message):
    lambda_client = boto3.client('lambda')
    request = {"message" : message}
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:891321150257:function:openai_invoke_api',
            InvocationType = 'RequestResponse',
            Payload=json.dumps(request).encode()
        )
    print(response['Payload'])
    terms = json.load(response['Payload'])['body']['response']
    return terms

def get_yelp_response(message):
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
    
def get_restaurant_response(message):
    lambda_client = boto3.client('lambda')
    request = {"body": "{  \"id\": \"" + message + "\"}"}
    print(request)
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:891321150257:function:GetRestaurantFromID',
            InvocationType = 'RequestResponse',
            Payload=json.dumps(request).encode()
        )
    print(response['Payload'])
    loaded = json.load(response['Payload'])
    aliases = loaded['restaurant_types']
    categories = loaded['restaurant_categories']
    terms = {"aliases" : aliases, "categories" : categories}
    return terms