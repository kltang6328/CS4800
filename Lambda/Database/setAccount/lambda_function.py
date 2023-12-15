import json
import boto3

client = boto3.client("dynamodb")
def lambda_handler(event, context):
    # TODO implement
    
    first_name = event["firstName"]
    last_name = event["lastName"]
    
    password = event["password"]
    email = event["email"]
    result = client.update_item(
        TableName = "account",
        Key = {"email":{"S":email}},
        UpdateExpression = "SET  password= :password,firstName = :first_name, lastName= :last_name",
        ExpressionAttributeValues = {
            
            
            ":password":{"S":password},
            ":first_name":{"S":first_name},
            ":last_name":{"S":last_name}
        },
        ReturnValues ="ALL_NEW" 
    )
    return {
        'statusCode': 200,
        'body': result["Attributes"]
    }
