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
    
    response = runtime.invoke_endpoint(EndpointName = 'image-classification-2022-07-03-02-06-14-908',
                                   ContentType='application/x-image',
                                   Body=image)
    
    result = json.loads(response['Body'].read().decode())


    # We return the data back to the Step Function    
    event["inferences"] = result
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }