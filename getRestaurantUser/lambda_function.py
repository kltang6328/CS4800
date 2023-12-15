import json
import boto3
client = boto3.client('dynamodb')
def lambda_handler(event, context):
    
    
    email = event["params"]["querystring"]["email"]
    
    result = client.get_item(
        TableName = "account",
        Key = {"email":{"S":email}},
        )
    
    # TODO implement
    return {
        'statusCode': 200,
        'restaurants': result["Item"]["likedRestaurants"]["L"]
    }