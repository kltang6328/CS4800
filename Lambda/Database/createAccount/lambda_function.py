import json
import boto3
import uuid
client = boto3.client('dynamodb')
def lambda_handler(event, context):
    
    first_name = event["firstName"]
    last_name = event["lastName"]
    
    password = event["password"]
    email = event["email"]
    
    
    account = {
        "email":{},
        
        "password":{},
        
        "firstName":{},
        "lastName":{},
        
        "likedRestaurants":{}
    }
    
    
    account["password"]["S"]=password
    account["firstName"]["S"] = first_name
    account["lastName"]["S"] = last_name
    account["email"]["S"] = email
    account["likedRestaurants"]["L"] = []
    
    client.put_item(
    TableName='account',
    Item=account
  )
    
    return {
        'statusCode': 300,
        'body': "successfully created account"
    }
