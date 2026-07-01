from botocore.exceptions import ClientError
from common.config import settings
import boto3

ses_client = boto3.client("ses", region_name=settings.aws_region)


def send_email(
    to_email: str, subject: str, html_body: str, text_body: str = ""
) -> bool:
    if not settings.ses_source_email:
        return False

    try:
        ses_client.send_email(
            Source=settings.ses_source_email,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Html": {"Data": html_body, "Charset": "UTF-8"},
                    "Text": {"Data": text_body or html_body, "Charset": "UTF-8"},
                },
            },
        )
        return True
    except ClientError:
        return False
