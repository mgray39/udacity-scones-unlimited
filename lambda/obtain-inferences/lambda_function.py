import json
import boto3
import base64

# Fill this in with the name of your deployed model
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