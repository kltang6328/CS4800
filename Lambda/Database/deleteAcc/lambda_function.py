import json
import boto3

client = boto3.client("dynamodb")
def lambda_handler(event, context):
    
    email = event["params"]["querystring"]["email"]
    data = client.delete_item(
        TableName = "account",
        Key= {'email':{"S":email}}
        )
    return {
        'statusCode': 200,
        'body': data
    }
