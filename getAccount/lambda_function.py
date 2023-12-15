import json
import boto3

client = boto3.client('dynamodb')
def lambda_handler(event, context):
    # TODO implement
    email = event["params"]["querystring"]["email"]
    data = client.get_item(TableName = 'account', Key= {'email':{"S":email}})
    if data.get("Item",None):
        return {"result":data["Item"]}
    else:
        return {"error":"email not found"}
    # {
    #     'statusCode': 200,
    #     'body': json.dumps(data["Item"])
    # }
