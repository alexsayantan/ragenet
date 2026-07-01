from botocore.exceptions import ClientError
from common.config import settings
import boto3
import json

sqs_client = boto3.client("sqs", region_name=settings.aws_region)


def send_email_message(
    to_email: str, subject: str, html_body: str, text_body: str = ""
) -> bool:
    if not settings.sqs_queue_url:
        return False

    try:
        sqs_client.send_message(
            QueueUrl=settings.sqs_queue_url,
            MessageBody=json.dumps(
                {
                    "to_email": to_email,
                    "subject": subject,
                    "html_body": html_body,
                    "text_body": text_body,
                }
            ),
        )
        return True
    except ClientError:
        return False
