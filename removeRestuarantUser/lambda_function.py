import json
import boto3
client = boto3.client('dynamodb')
def lambda_handler(event, context):
    
    
    email = event["params"]["querystring"]["email"]
    
    removeAll = event["params"]["querystring"].get("removeAll",False)
    if not removeAll:
        restaurantID = event["params"]["querystring"]["restaurantID"]
        removeID = {"S":restaurantID}
        result = client.get_item(
            TableName = "account",
            Key = {"email":{"S":email}},
            )
        rest = list(result["Item"]["likedRestaurants"]["L"])
        index = rest.index(removeID)
        removeExpression = "REMOVE likedRestaurants[%d]"%(index)
        result = client.update_item(
            TableName = "account",
            Key = {"email":{"S":email}},
            UpdateExpression=removeExpression,
            # ExpressionAttributeValues={
            #     ':restaurants':{"L":rest},  
            # },
            ReturnValues="ALL_NEW"
            )
        
        # TODO implement
        return {
            'statusCode': 200,
            'body': result
        }
    else:
        result = client.update_item(
            TableName = "account",
            Key = {"email":{"S":email}},
            UpdateExpression="SET likedRestaurants = :empty_value",
            ExpressionAttributeValues={
                ':empty_value':{"L":[]},  
            },
            ReturnValues="ALL_NEW"
            )
        
        # TODO implement
        return {
            'statusCode': 200,
            'body': result
        }
        