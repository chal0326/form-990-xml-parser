import boto3
import os
from settings.Settings import (
    cloudflare_r2_bucket_name,
    cloudflare_r2_access_key_id,
    cloudflare_r2_secret_access_key,
    cloudflare_r2_endpoint_url
)
from helpers.loggingutil import Log_Details, log_error, log_progress

class R2Manager:
    def __init__(self):
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=cloudflare_r2_endpoint_url,
                aws_access_key_id=cloudflare_r2_access_key_id,
                aws_secret_access_key=cloudflare_r2_secret_access_key
            )
            self.bucket_name = cloudflare_r2_bucket_name
        except Exception as e:
            log_error(e, "Failed to initialize R2 Client", Log_Details)

    def upload_file(self, file_path, object_name=None):
        """Upload a file to an S3 bucket (R2)"""

        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            log_progress('', f"Successfully uploaded {file_path} to R2 bucket {self.bucket_name} as {object_name}", Log_Details)
            return True
        except Exception as e:
            log_error(e, f"Failed to upload {file_path} to R2", Log_Details)
            return False

    def download_file(self, object_name, file_path):
        """Download a file from an S3 bucket (R2)"""
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            log_progress('', f"Successfully downloaded {object_name} from R2 bucket {self.bucket_name} to {file_path}", Log_Details)
            return True
        except Exception as e:
            log_error(e, f"Failed to download {object_name} from R2", Log_Details)
            return False
