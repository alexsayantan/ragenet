from common.email.sender import send_email
import json


def handler(event, context):
    for record in event.get("Records", []):
        try:
            body = json.loads(record["body"])
            send_email(
                to_email=body["to_email"],
                subject=body["subject"],
                html_body=body["html_body"],
                text_body=body.get("text_body", ""),
            )
        except (KeyError, json.JSONDecodeError):
            continue

    return {"statusCode": 200}
