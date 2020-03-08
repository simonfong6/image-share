#!/usr/bin/env python3
"""Uploading files to S3."""
import mimetypes
import os
import uuid

import boto3


BUCKET_NAME = 'image-share-public'
DIRECTORY = 'test'
FILE_FORM_NAME = 'file'


s3 = boto3.resource('s3')


def generate_unique_filename(filename):
    """Generates a unique filename with the correct extension."""

    uuid_ = uuid.uuid4()

    mime_type, _encoding = mimetypes.guess_type(filename)
    extension = mimetypes.guess_extension(mime_type)
    
    unique_filename = f"{uuid_}{extension}"

    return unique_filename

def upload_to_s3(key, file_to_upload, mime_type, bucket_name=BUCKET_NAME):
    """Uploads a file to S3."""
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(
        Key=key,
        Body=file_to_upload,
        ContentType=mime_type
    )

class FileUpload:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.bucket = s3.Bucket(bucket_name)

    def upload_to_s3(self, upload_file, path):
        """Upload to S3."""

        mime_type = FileUpload.get_mime_type(path)

        self.bucket.put_object(
            Key=path,
            Body=upload_file,
            ContentType=mime_type
        )
    
    def upload(self, upload_file, filename, directory=None):
        # Generate filename.
        unique_filename = generate_unique_filename(filename)

        mime_type = FileUpload.get_mime_type(filename)
        
        key = os.path.join(DIRECTORY, unique_filename)

        # Upload to S3.
        upload_to_s3(key, upload_file, mime_type)

    @staticmethod
    def get_mime_type(filename):
        """Gueses the mimetype of a file."""
        # Extract the MIME type.
        mime_type, _encoding = mimetypes.guess_type(filename)

        return mime_type

    def get_public_url(self, path):
        """Gets the public file url for a file with that path."""
        bucket_name = self.bucket_name
        public_url = f"https://{bucket_name}.s3-us-west-2.amazonaws.com/{path}"

        return public_url

    
