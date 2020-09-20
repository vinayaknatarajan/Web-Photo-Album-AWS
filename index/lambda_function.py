import json
import boto3
import time
from botocore.vendored import requests

def get_labels(bucket, key):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':key}})
    labels = [label['Name'] for label in response['Labels']]
    #print("sending shit")
    return labels
    
def index_into_es(index, type_doc, new_doc):
    #url = "https://vpc-photos-5vx3t2kil455h3jwjladddeybi.us-east-1.es.amazonaws.com"
    endpoint = 'https://vpc-photos-5vx3t2kil455h3jwjladddeybi.us-east-1.es.amazonaws.com/{}/{}'.format(index, type_doc)
    headers = {'Content-Type':'application/json'}
    print("before")
    res = requests.post(endpoint, data=new_doc, headers=headers)
    print("ress", res.content)
    
def lambda_handler(event, context):
    # TODO implement
    
    #response = rekognition.detect_labels(Image={'S3Object':{'Bucket':"storedphotos",'Name':"niceimage1.jpg"}})
    print(event)
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(bucket, key)
        labels = get_labels(bucket, key)
        print(labels)
        new_doc = {
            "objectKey": key,
            "bucket": bucket,
            "createdTimestamp": time.strftime("%Y%m%d-%H%M%S"),
            "labels": labels
        }
        print(new_doc)
        index_into_es('photos','photo',json.dumps(new_doc))
    
    return {
        'statusCode': 200,
        'body': json.dumps('It works!')
    }
