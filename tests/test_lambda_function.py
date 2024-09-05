import json
from lambda_function import lambda_handler

def test_lambda_handler():
    event = {
        'body': json.dumps({'user_id': 'test-user-id'})
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
