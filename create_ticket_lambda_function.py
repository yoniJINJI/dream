import json
import boto3
import uuid
from botocore.exceptions import ClientError

# Initialize the Cognito client
client = boto3.client('cognito-idp')

USER_POOL_ID = 'us-east-1_xp3CYcGcU'

def lambda_handler(event, context):
    # Parse the user_id from the request body (assuming it's in JSON format)
    body = json.loads(event['body'])
    user_id = body.get('user_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'user_id is required'})
        }

    try:
        # Search for the user by user_id (use either list_users or admin_get_user)
        user = get_user_by_id(user_id)

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
            
        # Generate a unique ticket ID
        ticket_id = str(uuid.uuid4())

        # Return the ticket ID in the response
        response = {
            'ticket_id': ticket_id,
            'user_id': user_id
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_user_by_id(user_id):
    """
    This function uses list_users to search for a user in the Cognito User Pool
    based on a custom attribute or user pool attribute.
    """
    try:
        # Search the User Pool by user_id using list_users
        response = client.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f"sub = \"{user_id}\""  # "sub" is the unique identifier in Cognito for users
        )
        # Return the first match if it exists
        if response['Users']:
            return response['Users'][0]
        return None

    except ClientError as e:
        print(f"Unable to search for user: {e}")
        raise e
