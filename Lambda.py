"""
This file is consolidated for the assessor in a single location with the specific file name requested

The actual scripts are in ./lambda/ sub-directories

#  Serialise image data

"""

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']

    s3.download_file(bucket, key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


"""
# Obtain Inference3s

Please not attribution of invocation of endpoint using boto3 to prevent the need to attempt to create a dummy package install and zip.

I attempted to do this, for the record.

But since sagemaker has no zip functionality and my own system was running a different flavour of linux and different distribution of python (I think I have 3.9) attempts to 
install into a local directory, either on my home machine or on the sagemaker instance produced an unmanageably large .zip file which couldn't be editted and threw errors 
like a monkey in a zoo throws bananas.

"""

import json
import boto3
import base64

# this function was rewritten after encountering the same problem as at https://knowledge.udacity.com/questions/753077
# and using the knowledge article provided as answer as an input into how to complete this


ENDPOINT = 'image-classification-2022-07-03-02-06-14-908'

runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])
    
    response = runtime.invoke_endpoint(EndpointName = ENDPOINT,
                                   ContentType='application/x-image',
                                   Body=image)
    
    result = json.loads(response['Body'].read().decode())


    # We return the data back to the Step Function    
    event["inferences"] = result
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


"""
# Check inferences above threshold

"""

import json


THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event['inferences']

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences)>THRESHOLD

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }