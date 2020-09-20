import json
import boto3
import time
from botocore.vendored import requests

def get_keywords(inputText):
    lex = boto3.client('lex-runtime')
    response = lex.post_text(
        botName = 'PhotoBot',
        botAlias = 'PhotoBot',
        userId = '12345',
        inputText = inputText
    )
    slots = response['slots']
    print("slots", slots)
    keywords = [v for _, v in slots.items() if v]
    print("keys=",keywords)
    return keywords
        
def get_image_locations(keywords):
    endpoint = 'https://vpc-photos-5vx3t2kil455h3jwjladddeybi.us-east-1.es.amazonaws.com/photos/_search'
    headers = {'Content-Type': 'application/json'}
    prepared_q = []
    for k in keywords:
        prepared_q.append({"match": {"labels": k}})
    q = {"query": {"bool": {"should": prepared_q}}}
    r = requests.post(endpoint, headers=headers, data=json.dumps(q))
    print("finding labels",r)
    image_array = []
    for each in r.json()['hits']['hits']:
        objectKey = each['_source']['objectKey']
        bucket = each['_source']['bucket']
        image_url = "https://" + bucket + ".s3.amazonaws.com/" + objectKey
        image_array.append(image_url)
    print(image_array)
    return image_array
    

def lambda_handler(event, context):
    # TODO implement
    inputText = event['queryStringParameters']['q']
    keywords = get_keywords(inputText)
    print(keywords)
    image_array = get_image_locations(keywords)
    image_array = list(set(image_array))
    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
        'body': json.dumps({"results":image_array})
    }
