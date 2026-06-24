import json


def signup(event, context):
    body = {
        "message": "Signup successful",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
