import json
import openai
from openai import OpenAI
import boto3

def get_api_key():
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:891321150257:function:openai_get_api_key',
            InvocationType = 'RequestResponse'
        )

    openai_api_key = json.load(response['Payload'])['body']['api_key']
    return openai_api_key

client = OpenAI(
    api_key=get_api_key()
)

def lambda_handler(event, context):
        
    openai.api_key = get_api_key()
    reccomender_params = """DO NOT RESPOND WITH A HELLO MESSAGE. You are a keyword extractor. The user will provide a request regarding the type of food they want. 
                            You will extract keywords related to food, prices, etc. 
                            If the user provides an address, consider it a single keyword. 
                            You will separate the keywords using the , symbol as a delimeter.
                            Exclude the following keywords: food; restaurant"""
    message_history = [{"role": "system", "content": reccomender_params}]
    
    message_history.append({"role": "user", "content": event["message"]})
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages = message_history
    )
    text_response = completion.choices[0].message.content
    return {
        'statusCode':200,
        "headers" : {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
        },
        'body': {
            'response' : text_response
        }
    }