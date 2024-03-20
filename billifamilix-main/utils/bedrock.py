import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv('.env',
            verbose=False)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Define a function to call the bedrock API for code summarization
def call_bedrock(code):
    # Call the Bedrock client
    bedrock = boto3.client(service_name='bedrock-runtime',
                           region_name='us-east-1',
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Tweak your preferred model parameters, prompt and assistant information
    body = json.dumps({
        "prompt": f"\n\nHuman: Explain functionalities of the following Java code segment in a couple of bullet points {code}\n\nAssistant: Explain well to a non-technical person what is happening within the provided code",
        "max_tokens_to_sample": 500,
        "temperature": 0.2,
        "top_p": 0.9,})

    # Define the type of model that will be used
    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    # Call the Bedrock API
    response = bedrock.invoke_model(body=body,
                                    modelId=modelId,
                                    accept=accept,
                                    contentType=contentType)
    response_body = json.loads(response.get('body').read())
    print(response_body.get('completion'))

    return response_body.get('completion')

# Test out the call_bedrock function
# call_bedrock("Enter")


def ask_llm(
        instruction = "",
        data = "",
        question = "",
        modelId = 'anthropic.claude-v2',
        service_name = 'bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=AWS_SECRET_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        ):
    
    bedrock = boto3.client(service_name=service_name,
                           region_name=region_name,
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key)

    # Tweak your preferred model parameters, prompt and assistant information
    body = json.dumps({
        "prompt": f"\n\nHuman: {instruction}\n\n{data}\n\n{question} \n\n Assistant:",
        "max_tokens_to_sample": 500,
        "temperature": 0.2,
        "top_p": 0.9,})
    
    accept = 'application/json'
    contentType = 'application/json'

    # Call the Bedrock API
    response = bedrock.invoke_model(body=body,
                                    modelId=modelId,
                                    accept=accept,
                                    contentType=contentType)
    response_body = json.loads(response.get('body').read())
    # print(response_body.get('completion'))

    return response_body.get('completion')