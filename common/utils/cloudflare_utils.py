from botocore.config import Config
from common.config import settings
import boto3


class CloudflareR2Client:
    def __init__(self):
        self.account_id = settings.cloudflare_account_id
        self.access_key_id = settings.cloudflare_r2_access_key_id
        self.secret_access_key = settings.cloudflare_r2_secret_access_key
        self.bucket_name = settings.cloudflare_r2_bucket_name
        self.public_url = settings.cloudflare_r2_public_url

        self.client = boto3.client(
            "s3",
            endpoint_url=f"https://{self.account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def upload_file(self, file_name: str, file_content: bytes, content_type: str = "application/octet-stream") -> str:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=file_content,
            ContentType=content_type,
        )
        return f"{self.public_url}/{file_name}"

    def get_file(self, file_name: str) -> bytes | None:
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=file_name)
            return response["Body"].read()
        except self.client.exceptions.NoSuchKey:
            return None

    def delete_file(self, file_name: str) -> None:
        self.client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def list_files(self, prefix: str = "") -> list[str]:
        response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]

    def upload_files(self, files: dict[str, bytes], content_type: str = "application/octet-stream") -> dict[str, str]:
        urls = {}
        for file_name, file_content in files.items():
            urls[file_name] = self.upload_file(file_name, file_content, content_type)
        return urls

    def delete_files(self, file_names: list[str]) -> None:
        objects = [{"Key": name} for name in file_names]
        self.client.delete_objects(
            Bucket=self.bucket_name,
            Delete={"Objects": objects},
        )

    def get_files(self, file_names: list[str]) -> dict[str, bytes | None]:
        results = {}
        for name in file_names:
            results[name] = self.get_file(name)
        return results

    def delete_files_by_prefix(self, prefix: str) -> None:
        file_names = self.list_files(prefix)
        if file_names:
            self.delete_files(file_names)


r2_client = CloudflareR2Client()
