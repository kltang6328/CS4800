import json
import boto3
client = boto3.client('dynamodb')
def lambda_handler(event, context):
    email = event["email"]
    
    restaurantID = event["restaurantID"]
    
    result = client.update_item(
        TableName = "account",
        Key = {"email":{"S":email}},
        UpdateExpression="SET likedRestaurants = list_append(likedRestaurants, :restID)",
        ExpressionAttributeValues={
            ':restID':{"L":[{"S":str(restaurantID)}]},
        },
        ReturnValues="UPDATED_NEW"
        )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
