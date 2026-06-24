import json


def signin(event, context):
    body = {
        "message": "Signin successful",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
